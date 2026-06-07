#!/usr/bin/env python3
"""
Tactical Legends - Complete Python Implementation
A turn-based tactical strategy game with squad customization and dynamic missions.
"""

import pygame
import random
import math
import json
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple, Dict, Set
from abc import ABC, abstractmethod
import sys
from pathlib import Path

# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 40

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (64, 64, 64)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_ORANGE = (255, 165, 0)

# ============================================================================
# ENUMERATIONS
# ============================================================================

class UnitType(Enum):
    """Available unit types in the game."""
    SOLDIER = "soldier"
    SCOUT = "scout"
    HEAVY = "heavy"
    MEDIC = "medic"
    SPECIALIST = "specialist"

class UnitTeam(Enum):
    """Team alignment."""
    PLAYER = "player"
    ENEMY = "enemy"
    NEUTRAL = "neutral"

class TileType(Enum):
    """Types of tiles on the map."""
    GRASS = "grass"
    WATER = "water"
    MOUNTAIN = "mountain"
    FOREST = "forest"
    BUILDING = "building"
    ROAD = "road"

class ActionType(Enum):
    """Types of actions a unit can perform."""
    MOVE = "move"
    ATTACK = "attack"
    DEFEND = "defend"
    ABILITY = "ability"
    WAIT = "wait"

class GameState(Enum):
    """Main game states."""
    MENU = "menu"
    MISSION_SELECT = "mission_select"
    BATTLE = "battle"
    UNIT_SELECT = "unit_select"
    GAME_OVER = "game_over"

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Position:
    """Represents a position on the map."""
    x: int
    y: int
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate Euclidean distance to another position."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return isinstance(other, Position) and self.x == other.x and self.y == other.y

@dataclass
class Stats:
    """Unit statistics."""
    health: int = 100
    max_health: int = 100
    damage: int = 10
    defense: int = 5
    accuracy: int = 80
    mobility: int = 5
    
    def take_damage(self, damage: int) -> int:
        """Reduce health and return damage taken."""
        actual_damage = max(1, damage - self.defense)
        self.health = max(0, self.health - actual_damage)
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Heal and return amount healed."""
        healed = min(amount, self.max_health - self.health)
        self.health += healed
        return healed

@dataclass
class Unit:
    """Represents a game unit."""
    id: str
    name: str
    unit_type: UnitType
    team: UnitTeam
    position: Position
    stats: Stats = field(default_factory=Stats)
    action_points: int = 3
    max_action_points: int = 3
    is_alive: bool = True
    experience: int = 0
    level: int = 1
    
    def get_attack_range(self) -> int:
        """Get attack range based on unit type."""
        ranges = {
            UnitType.SOLDIER: 1,
            UnitType.SCOUT: 2,
            UnitType.HEAVY: 1,
            UnitType.MEDIC: 1,
            UnitType.SPECIALIST: 3,
        }
        return ranges.get(self.unit_type, 1)
    
    def can_move_to(self, target: Position, map_grid: 'Map') -> bool:
        """Check if unit can move to target position."""
        if not map_grid.is_walkable(target):
            return False
        distance = self.position.distance_to(target)
        return distance <= self.stats.mobility and self.action_points >= 1
    
    def move_to(self, target: Position) -> bool:
        """Move unit to target position."""
        if self.can_move_to(target, None):  # Map validation would go here
            self.position = target
            self.action_points -= 1
            return True
        return False
    
    def gain_experience(self, amount: int):
        """Gain experience and handle leveling."""
        self.experience += amount
        if self.experience >= 100 * self.level:
            self.level_up()
    
    def level_up(self):
        """Increase unit level and stats."""
        self.level += 1
        self.stats.max_health += 10
        self.stats.health = self.stats.max_health
        self.stats.damage += 2
        self.stats.defense += 1
    
    def end_turn(self):
        """Reset action points for next turn."""
        self.action_points = self.max_action_points
    
    def take_damage(self, damage: int) -> int:
        """Take damage and check if dead."""
        actual_damage = self.stats.take_damage(damage)
        if self.stats.health <= 0:
            self.is_alive = False
        return actual_damage

# ============================================================================
# MAP & TILE SYSTEM
# ============================================================================

@dataclass
class Tile:
    """Represents a single tile on the map."""
    position: Position
    tile_type: TileType
    is_walkable: bool = True
    occupant: Optional[Unit] = None
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get color for rendering."""
        colors = {
            TileType.GRASS: (34, 139, 34),
            TileType.WATER: (65, 105, 225),
            TileType.MOUNTAIN: (169, 169, 169),
            TileType.FOREST: (0, 100, 0),
            TileType.BUILDING: (139, 69, 19),
            TileType.ROAD: (210, 180, 140),
        }
        return colors.get(self.tile_type, COLOR_GRAY)

class Map:
    """Game map with tiles and navigation."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles: Dict[Position, Tile] = {}
        self._generate_map()
    
    def _generate_map(self):
        """Generate a random map."""
        for x in range(self.width):
            for y in range(self.height):
                pos = Position(x, y)
                # Random terrain generation
                rand = random.random()
                if rand < 0.7:
                    tile_type = TileType.GRASS
                elif rand < 0.85:
                    tile_type = TileType.FOREST
                elif rand < 0.95:
                    tile_type = TileType.MOUNTAIN
                else:
                    tile_type = TileType.WATER
                
                is_walkable = tile_type != TileType.WATER and tile_type != TileType.MOUNTAIN
                self.tiles[pos] = Tile(pos, tile_type, is_walkable)
    
    def get_tile(self, pos: Position) -> Optional[Tile]:
        """Get tile at position."""
        return self.tiles.get(pos)
    
    def is_walkable(self, pos: Position) -> bool:
        """Check if position is walkable."""
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            tile = self.get_tile(pos)
            return tile and tile.is_walkable and tile.occupant is None
        return False
    
    def get_units_in_range(self, pos: Position, range_val: int) -> List[Unit]:
        """Get all units within range of position."""
        units = []
        for tile in self.tiles.values():
            if tile.occupant and pos.distance_to(tile.position) <= range_val:
                units.append(tile.occupant)
        return units
    
    def place_unit(self, unit: Unit, pos: Position) -> bool:
        """Place unit on map."""
        tile = self.get_tile(pos)
        if tile and tile.is_walkable and tile.occupant is None:
            tile.occupant = unit
            unit.position = pos
            return True
        return False
    
    def remove_unit(self, pos: Position):
        """Remove unit from map."""
        tile = self.get_tile(pos)
        if tile:
            tile.occupant = None

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class CombatSystem:
    """Handles all combat calculations and resolution."""
    
    @staticmethod
    def calculate_hit_chance(attacker: Unit, defender: Unit, distance: float) -> float:
        """Calculate probability of hit."""
        base_accuracy = attacker.stats.accuracy / 100.0
        distance_penalty = max(0, (distance - 1) * 0.1)
        defense_bonus = defender.stats.defense / 100.0
        
        hit_chance = base_accuracy - distance_penalty - defense_bonus
        return max(0.1, min(1.0, hit_chance))
    
    @staticmethod
    def calculate_damage(attacker: Unit, defender: Unit) -> int:
        """Calculate damage dealt."""
        base_damage = attacker.stats.damage
        variance = random.randint(-5, 5)
        defense_reduction = defender.stats.defense // 2
        
        total_damage = base_damage + variance - defense_reduction
        return max(1, total_damage)
    
    @staticmethod
    def resolve_attack(attacker: Unit, defender: Unit, map_grid: 'Map') -> Dict:
        """Resolve a single attack."""
        distance = attacker.position.distance_to(defender.position)
        
        # Check if in range
        if distance > attacker.get_attack_range():
            return {"hit": False, "message": "Target out of range", "damage": 0}
        
        # Check action points
        if attacker.action_points < 1:
            return {"hit": False, "message": "Not enough action points", "damage": 0}
        
        # Calculate hit
        hit_chance = CombatSystem.calculate_hit_chance(attacker, defender, distance)
        hit = random.random() < hit_chance
        
        if hit:
            damage = CombatSystem.calculate_damage(attacker, defender)
            actual_damage = defender.take_damage(damage)
            attacker.action_points -= 1
            attacker.gain_experience(25)
            
            return {
                "hit": True,
                "message": f"{attacker.name} hits {defender.name} for {actual_damage} damage!",
                "damage": actual_damage,
                "defender_alive": defender.is_alive
            }
        else:
            attacker.action_points -= 1
            return {
                "hit": False,
                "message": f"{attacker.name} missed!",
                "damage": 0
            }

# ============================================================================
# AI SYSTEM
# ============================================================================

class AIController:
    """Controls enemy unit behavior."""
    
    def __init__(self, unit: Unit):
        self.unit = unit
    
    def get_best_action(self, allies: List[Unit], enemies: List[Unit], 
                       map_grid: 'Map') -> Optional[Tuple[ActionType, Position]]:
        """Determine best action for this unit."""
        if not self.unit.is_alive:
            return None
        
        # Find closest enemy
        closest_enemy = None
        closest_distance = float('inf')
        
        for enemy in enemies:
            if enemy.is_alive:
                distance = self.unit.position.distance_to(enemy.position)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy
        
        if not closest_enemy:
            return None
        
        # Try to move closer and attack
        attack_range = self.unit.get_attack_range()
        
        if closest_distance <= attack_range:
            return (ActionType.ATTACK, closest_enemy.position)
        else:
            # Move towards enemy
            direction = self._get_direction_towards(closest_enemy.position)
            new_pos = Position(
                self.unit.position.x + direction[0],
                self.unit.position.y + direction[1]
            )
            if map_grid.is_walkable(new_pos):
                return (ActionType.MOVE, new_pos)
        
        return (ActionType.WAIT, self.unit.position)
    
    def _get_direction_towards(self, target: Position) -> Tuple[int, int]:
        """Get direction vector towards target."""
        dx = target.x - self.unit.position.x
        dy = target.y - self.unit.position.y
        
        dir_x = 1 if dx > 0 else (-1 if dx < 0 else 0)
        dir_y = 1 if dy > 0 else (-1 if dy < 0 else 0)
        
        return (dir_x, dir_y)

# ============================================================================
# MISSION SYSTEM
# ============================================================================

@dataclass
class Mission:
    """Represents a mission."""
    id: str
    name: str
    description: str
    map_width: int = 20
    map_height: int = 15
    difficulty: int = 1
    reward_exp: int = 100
    reward_gold: int = 500
    objective: str = "Defeat all enemies"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

class MissionManager:
    """Manages available missions."""
    
    def __init__(self):
        self.missions = self._create_missions()
    
    def _create_missions(self) -> List[Mission]:
        """Create default missions."""
        return [
            Mission(
                id="mission_1",
                name="Infiltration",
                description="Sneak past enemy lines and reach the objective.",
                difficulty=1,
                reward_exp=100,
                reward_gold=500
            ),
            Mission(
                id="mission_2",
                name="Defensive Stand",
                description="Hold position against incoming enemy forces.",
                difficulty=2,
                reward_exp=200,
                reward_gold=1000
            ),
            Mission(
                id="mission_3",
                name="Assassination",
                description="Eliminate the target unit without being detected.",
                difficulty=3,
                reward_exp=300,
                reward_gold=1500
            ),
        ]
    
    def get_mission(self, mission_id: str) -> Optional[Mission]:
        """Get mission by ID."""
        return next((m for m in self.missions if m.id == mission_id), None)

# ============================================================================
# PLAYER SQUAD MANAGEMENT
# ============================================================================

@dataclass
class Squad:
    """Player's squad of units."""
    name: str
    units: List[Unit] = field(default_factory=list)
    level: int = 1
    experience: int = 0
    gold: int = 1000
    
    def add_unit(self, unit: Unit):
        """Add unit to squad."""
        self.units.append(unit)
    
    def remove_unit(self, unit_id: str):
        """Remove unit from squad."""
        self.units = [u for u in self.units if u.id != unit_id]
    
    def get_alive_units(self) -> List[Unit]:
        """Get all alive units."""
        return [u for u in self.units if u.is_alive]
    
    def gain_gold(self, amount: int):
        """Gain gold."""
        self.gold += amount
    
    def spend_gold(self, amount: int) -> bool:
        """Spend gold if available."""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

class SquadBuilder:
    """Helps create and customize squads."""
    
    @staticmethod
    def create_default_squad() -> Squad:
        """Create a default player squad."""
        squad = Squad(name="Elite Squadron")
        
        # Add default units
        units_config = [
            ("soldier_1", "Alpha", UnitType.SOLDIER),
            ("scout_1", "Scout One", UnitType.SCOUT),
            ("heavy_1", "Tank", UnitType.HEAVY),
            ("medic_1", "Doc", UnitType.MEDIC),
        ]
        
        for unit_id, name, unit_type in units_config:
            unit = Unit(
                id=unit_id,
                name=name,
                unit_type=unit_type,
                team=UnitTeam.PLAYER,
                position=Position(0, 0),
                stats=SquadBuilder._get_unit_stats(unit_type)
            )
            squad.add_unit(unit)
        
        return squad
    
    @staticmethod
    def _get_unit_stats(unit_type: UnitType) -> Stats:
        """Get base stats for unit type."""
        stats_config = {
            UnitType.SOLDIER: Stats(health=100, max_health=100, damage=12, defense=5, accuracy=80, mobility=4),
            UnitType.SCOUT: Stats(health=70, max_health=70, damage=8, defense=2, accuracy=90, mobility=6),
            UnitType.HEAVY: Stats(health=150, max_health=150, damage=15, defense=10, accuracy=70, mobility=2),
            UnitType.MEDIC: Stats(health=80, max_health=80, damage=5, defense=3, accuracy=70, mobility=4),
            UnitType.SPECIALIST: Stats(health=90, max_health=90, damage=10, defense=4, accuracy=85, mobility=5),
        }
        return stats_config.get(unit_type, Stats())

# ============================================================================
# BATTLE SYSTEM
# ============================================================================

class Battle:
    """Manages a single battle."""
    
    def __init__(self, mission: Mission, player_squad: Squad):
        self.mission = mission
        self.player_squad = player_squad
        self.map = Map(mission.map_width, mission.map_height)
        self.all_units: List[Unit] = []
        self.current_turn = 0
        self.is_player_turn = True
        self.is_active = True
        self.message_log: List[str] = []
        
        self._initialize_battle()
    
    def _initialize_battle(self):
        """Set up the battle."""
        # Place player units
        for i, unit in enumerate(self.player_squad.units):
            start_pos = Position(1 + i * 2, 1)
            unit.is_alive = True
            unit.stats.health = unit.stats.max_health
            unit.end_turn()
            self.map.place_unit(unit, start_pos)
            self.all_units.append(unit)
        
        # Create and place enemy units
        enemy_count = 2 + self.mission.difficulty
        for i in range(enemy_count):
            enemy = Unit(
                id=f"enemy_{i}",
                name=f"Enemy {i+1}",
                unit_type=random.choice(list(UnitType)),
                team=UnitTeam.ENEMY,
                position=Position(0, 0),
                stats=SquadBuilder._get_unit_stats(random.choice(list(UnitType)))
            )
            enemy_pos = Position(
                self.map.width - 3 - i * 2,
                self.map.height - 2
            )
            self.map.place_unit(enemy, enemy_pos)
            self.all_units.append(enemy)
        
        self.add_message("Battle started!")
    
    def add_message(self, message: str):
        """Add message to log."""
        self.message_log.append(message)
        if len(self.message_log) > 10:
            self.message_log.pop(0)
    
    def get_player_units(self) -> List[Unit]:
        """Get all alive player units."""
        return [u for u in self.all_units if u.team == UnitTeam.PLAYER and u.is_alive]
    
    def get_enemy_units(self) -> List[Unit]:
        """Get all alive enemy units."""
        return [u for u in self.all_units if u.team == UnitTeam.ENEMY and u.is_alive]
    
    def check_victory(self) -> Optional[str]:
        """Check if battle is won/lost."""
        player_units = self.get_player_units()
        enemy_units = self.get_enemy_units()
        
        if not player_units:
            return "DEFEAT"
        if not enemy_units:
            return "VICTORY"
        return None
    
    def move_unit(self, unit: Unit, target_pos: Position) -> bool:
        """Move a unit to target position."""
        if not unit.is_alive or unit.action_points < 1:
            return False
        
        if not self.map.is_walkable(target_pos):
            self.add_message(f"{unit.name} cannot move there!")
            return False
        
        distance = unit.position.distance_to(target_pos)
        if distance > unit.stats.mobility:
            self.add_message(f"{unit.name} cannot reach that position!")
            return False
        
        self.map.remove_unit(unit.position)
        self.map.place_unit(unit, target_pos)
        unit.action_points -= 1
        self.add_message(f"{unit.name} moved to ({target_pos.x}, {target_pos.y})")
        return True
    
    def attack_unit(self, attacker: Unit, defender: Unit) -> bool:
        """Attack a unit."""
        if not attacker.is_alive or not defender.is_alive:
            return False
        
        result = CombatSystem.resolve_attack(attacker, defender, self.map)
        self.add_message(result["message"])
        
        if not defender.is_alive:
            self.map.remove_unit(defender.position)
        
        return result["hit"]
    
    def end_player_turn(self):
        """End player turn and start enemy turn."""
        for unit in self.get_player_units():
            unit.end_turn()
        
        self.is_player_turn = False
        self.execute_enemy_turns()
    
    def execute_enemy_turns(self):
        """Execute AI turns for all enemies."""
        for enemy in self.get_enemy_units():
            action, target_pos = self._get_enemy_action(enemy)
            
            if action == ActionType.MOVE:
                self.move_unit(enemy, target_pos)
            elif action == ActionType.ATTACK:
                # Find enemy at target position
                target_unit = self.map.get_tile(target_pos).occupant
                if target_unit and target_unit != enemy:
                    self.attack_unit(enemy, target_unit)
            
            enemy.end_turn()
        
        self.is_player_turn = True
        self.current_turn += 1
    
    def _get_enemy_action(self, enemy: Unit) -> Tuple[ActionType, Position]:
        """Get action for enemy unit."""
        controller = AIController(enemy)
        action, target_pos = controller.get_best_action(
            self.get_enemy_units(),
            self.get_player_units(),
            self.map
        ) or (ActionType.WAIT, enemy.position)
        return (action, target_pos)

# ============================================================================
# RENDERING SYSTEM
# ============================================================================

class Renderer:
    """Handles all rendering."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_large = pygame.font.Font(None, 48)
    
    def render_battle(self, battle: Battle):
        """Render battle scene."""
        self.screen.fill(COLOR_BLACK)
        
        # Draw map
        self._render_map(battle.map)
        
        # Draw units
        self._render_units(battle.all_units)
        
        # Draw UI
        self._render_battle_ui(battle)
    
    def _render_map(self, map_grid: Map):
        """Render the game map."""
        for tile in map_grid.tiles.values():
            x = tile.position.x * TILE_SIZE
            y = tile.position.y * TILE_SIZE
            color = tile.get_color()
            pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(self.screen, COLOR_GRAY, (x, y, TILE_SIZE, TILE_SIZE), 1)
    
    def _render_units(self, units: List[Unit]):
        """Render all units."""
        for unit in units:
            if unit.is_alive:
                x = unit.position.x * TILE_SIZE + TILE_SIZE // 2
                y = unit.position.y * TILE_SIZE + TILE_SIZE // 2
                
                # Draw circle for unit
                color = COLOR_BLUE if unit.team == UnitTeam.PLAYER else COLOR_RED
                pygame.draw.circle(self.screen, color, (x, y), TILE_SIZE // 3)
                
                # Draw health bar
                health_bar_width = TILE_SIZE - 4
                health_bar_height = 4
                health_percent = unit.stats.health / unit.stats.max_health
                
                pygame.draw.rect(
                    self.screen,
                    COLOR_RED,
                    (unit.position.x * TILE_SIZE + 2,
                     unit.position.y * TILE_SIZE + 2,
                     health_bar_width,
                     health_bar_height)
                )
                pygame.draw.rect(
                    self.screen,
                    COLOR_GREEN,
                    (unit.position.x * TILE_SIZE + 2,
                     unit.position.y * TILE_SIZE + 2,
                     health_bar_width * health_percent,
                     health_bar_height)
                )
    
    def _render_battle_ui(self, battle: Battle):
        """Render battle UI elements."""
        # Draw message log
        log_x = 10
        log_y = SCREEN_HEIGHT - 150
        
        pygame.draw.rect(self.screen, COLOR_DARK_GRAY, (log_x, log_y, SCREEN_WIDTH - 20, 140))
        
        for i, message in enumerate(battle.message_log[-5:]):
            text = self.font_small.render(message, True, COLOR_WHITE)
            self.screen.blit(text, (log_x + 5, log_y + 5 + i * 25))
        
        # Draw turn info
        turn_text = self.font_medium.render(f"Turn: {battle.current_turn}", True, COLOR_YELLOW)
        self.screen.blit(turn_text, (10, 10))
        
        # Draw player units info
        info_text = f"Units: {len(battle.get_player_units())}/{len(battle.player_squad.units)}"
        info_surface = self.font_small.render(info_text, True, COLOR_GREEN)
        self.screen.blit(info_surface, (10, 50))
        
        # Draw victory/defeat message
        result = battle.check_victory()
        if result:
            result_color = COLOR_GREEN if result == "VICTORY" else COLOR_RED
            result_text = self.font_large.render(result, True, result_color)
            text_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(result_text, text_rect)
    
    def render_menu(self):
        """Render main menu."""
        self.screen.fill(COLOR_BLACK)
        
        title = self.font_large.render("TACTICAL LEGENDS", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_medium.render("Rise of OISTARIAN", True, COLOR_YELLOW)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(subtitle, subtitle_rect)
        
        start_text = self.font_medium.render("Press SPACE to Start", True, COLOR_WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(start_text, start_rect)
        
        exit_text = self.font_small.render("Press ESC to Exit", True, COLOR_GRAY)
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(exit_text, exit_rect)

# ============================================================================
# GAME CONTROLLER
# ============================================================================

class GameController:
    """Main game controller."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tactical Legends - Rise of OISTARIAN")
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        
        self.state = GameState.MENU
        self.running = True
        
        self.mission_manager = MissionManager()
        self.player_squad = SquadBuilder.create_default_squad()
        self.current_battle: Optional[Battle] = None
        self.selected_unit: Optional[Unit] = None
    
    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)
    
    def _handle_keydown(self, event: pygame.event.Event):
        """Handle keyboard input."""
        if event.key == pygame.K_ESCAPE:
            if self.state == GameState.BATTLE:
                self.state = GameState.MISSION_SELECT
                self.current_battle = None
            else:
                self.running = False
        elif event.key == pygame.K_SPACE:
            if self.state == GameState.MENU:
                self.state = GameState.MISSION_SELECT
            elif self.state == GameState.MISSION_SELECT:
                # Start first mission
                mission = self.mission_manager.get_mission("mission_1")
                self.current_battle = Battle(mission, self.player_squad)
                self.state = GameState.BATTLE
        elif event.key == pygame.K_RETURN:
            if self.state == GameState.BATTLE and self.current_battle:
                self.current_battle.end_player_turn()
    
    def _handle_mouse_click(self, event: pygame.event.Event):
        """Handle mouse clicks."""
        if self.state == GameState.BATTLE and self.current_battle:
            x, y = event.pos
            tile_x = x // TILE_SIZE
            tile_y = y // TILE_SIZE
            
            # Select unit if clicked on player unit
            tile = self.current_battle.map.get_tile(Position(tile_x, tile_y))
            if tile and tile.occupant:
                if tile.occupant.team == UnitTeam.PLAYER:
                    self.selected_unit = tile.occupant
                elif self.selected_unit:
                    # Attack enemy
                    self.current_battle.attack_unit(self.selected_unit, tile.occupant)
            elif self.selected_unit:
                # Move selected unit
                self.current_battle.move_unit(self.selected_unit, Position(tile_x, tile_y))
    
    def update(self):
        """Update game logic."""
        if self.state == GameState.BATTLE and self.current_battle:
            # Check for battle end
            result = self.current_battle.check_victory()
            if result:
                if result == "VICTORY":
                    self.player_squad.gain_gold(self.current_battle.mission.reward_gold)
                    self.current_battle.add_message(f"Mission Complete! +{self.current_battle.mission.reward_gold} gold")
                self.state = GameState.GAME_OVER
    
    def render(self):
        """Render game."""
        if self.state == GameState.MENU:
            self.renderer.render_menu()
        elif self.state == GameState.BATTLE and self.current_battle:
            self.renderer.render_battle(self.current_battle)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point."""
    game = GameController()
    game.run()

if __name__ == "__main__":
    main()
