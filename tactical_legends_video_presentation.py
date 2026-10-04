#!/usr/bin/env python3
"""
Tactical Legends: Rise of OISTARIAN - Video Presentation Generator
Converts the trailer script into an interactive video presentation using Pygame
"""

import pygame
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import math

# ============================================================================
# CONFIGURATION
# ============================================================================

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
FONT_PATH = "assets/fonts/consolas.ttf"  # Fallback to system fonts

class SceneType(Enum):
    """Scene types in the presentation"""
    BLACK_SCREEN = 0
    FLASH_CUTS = 1
    COMBAT_SEQUENCE = 2
    MONTAGE = 3
    FINAL_REVEAL = 4
    CREDITS = 5

@dataclass
class Scene:
    """A scene in the presentation"""
    name: str
    duration: float  # seconds
    scene_type: SceneType
    narration_text: str
    background_color: tuple
    effects: List[str]

# ============================================================================
# VISUAL EFFECTS
# ============================================================================

class ParticleEffect:
    """Particle effect renderer"""
    def __init__(self, x: float, y: float, color: tuple, lifetime: float):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.age = 0
        self.vx = (math.cos(math.radians(self.age)) * 2)
        self.vy = (math.sin(math.radians(self.age)) * 2)
        self.size = 5

    def update(self, dt: float):
        self.age += dt
        self.x += self.vx
        self.y += self.vy
        self.size = max(0, 5 * (1 - self.age / self.lifetime))

    def is_alive(self) -> bool:
        return self.age < self.lifetime

    def draw(self, surface: pygame.Surface):
        if self.size > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class GlitchEffect:
    """Screen glitch effect"""
    def __init__(self, intensity: float = 0.05):
        self.intensity = intensity
        self.offset_x = 0
        self.offset_y = 0
        self.time = 0

    def update(self, dt: float):
        self.time += dt
        if math.sin(self.time * 20) > 0.5:  # Glitch timing
            self.offset_x = int((math.random() - 0.5) * 20 * self.intensity)
            self.offset_y = int((math.random() - 0.5) * 20 * self.intensity)

    def apply(self, surface: pygame.Surface) -> pygame.Surface:
        return surface

class NeonFlash:
    """Neon flash effect"""
    def __init__(self, duration: float):
        self.duration = duration
        self.age = 0
        self.intensity = 0

    def update(self, dt: float):
        self.age += dt
        # Intensity oscillates from 0 to 1 to 0
        progress = self.age / self.duration
        self.intensity = math.sin(progress * math.pi) if progress <= 1 else 0

    def is_active(self) -> bool:
        return self.age < self.duration

    def get_overlay_color(self) -> tuple:
        alpha = int(255 * self.intensity * 0.3)
        return (0, 255, 255, alpha)  # Cyan neon

# ============================================================================
# TEXT RENDERING
# ============================================================================

class TextRenderer:
    """Handles text rendering with effects"""
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.fonts = {}
        self._load_fonts()

    def _load_fonts(self):
        """Load or create fonts"""
        try:
            self.fonts['narration'] = pygame.font.SysFont("consolas", 48, bold=True)
            self.fonts['subtitle'] = pygame.font.SysFont("consolas", 36)
            self.fonts['tagline'] = pygame.font.SysFont("impact", 72, bold=True)
        except:
            # Fallback to default font
            self.fonts['narration'] = pygame.font.Font(None, 48)
            self.fonts['subtitle'] = pygame.font.Font(None, 36)
            self.fonts['tagline'] = pygame.font.Font(None, 72)

    def render_narration(self, text: str, opacity: float = 1.0) -> pygame.Surface:
        """Render narration text with opacity"""
        font = self.fonts['narration']
        rendered = font.render(text, True, (200, 200, 200))
        rendered.set_alpha(int(255 * opacity))
        return rendered

    def render_tagline(self, text: str, color: tuple = (255, 215, 0)) -> pygame.Surface:
        """Render tagline with color"""
        font = self.fonts['tagline']
        return font.render(text, True, color)

    def render_centered(self, surface: pygame.Surface, text_surface: pygame.Surface, y_offset: float = 0):
        """Render text centered on screen"""
        x = (self.screen.get_width() - text_surface.get_width()) // 2
        y = (self.screen.get_height() - text_surface.get_height()) // 2 + y_offset
        self.screen.blit(text_surface, (x, y))

# ============================================================================
# SCENE MANAGERS
# ============================================================================

class SceneManager:
    """Manages scene transitions and timing"""
    def __init__(self):
        self.scenes = self._create_scenes()
        self.current_scene_index = 0
        self.scene_timer = 0
        self.total_time = 0

    def _create_scenes(self) -> List[Scene]:
        """Create all scenes for the presentation"""
        return [
            Scene(
                name="Opening - Black Screen",
                duration=3.0,
                scene_type=SceneType.BLACK_SCREEN,
                narration_text="In a world coded in silence... one whisper rewrites the algorithm.",
                background_color=(0, 0, 0),
                effects=["fade_in_text", "data_pulse"]
            ),
            Scene(
                name="Flash Cuts",
                duration=4.0,
                scene_type=SceneType.FLASH_CUTS,
                narration_text="They said you were erased, but legends don't vanish. They reload.",
                background_color=(20, 20, 40),
                effects=["memory_crystal_shatter", "neon_glitch", "drone_flash"]
            ),
            Scene(
                name="Combat Sequence",
                duration=5.0,
                scene_type=SceneType.COMBAT_SEQUENCE,
                narration_text="OISTARIAN—former engineer. Reluctant operative. Relentless myth.",
                background_color=(40, 10, 20),
                effects=["explosion_bloom", "neon_flash", "combat_sync"]
            ),
            Scene(
                name="Fast Montage",
                duration=4.5,
                scene_type=SceneType.MONTAGE,
                narration_text="Encrypted data walls exploding. The vault marked EDEN unlocking.",
                background_color=(30, 30, 50),
                effects=["data_wall_explosion", "vault_unlock", "hologram_flicker"]
            ),
            Scene(
                name="Final Reveal",
                duration=3.5,
                scene_type=SceneType.FINAL_REVEAL,
                narration_text="This time, I choose the ending.",
                background_color=(60, 30, 80),
                effects=["storm_lighting", "silhouette_reveal", "neon_fade"]
            ),
            Scene(
                name="Tagline",
                duration=3.0,
                scene_type=SceneType.CREDITS,
                narration_text="Tactical Legends: Rise of OISTARIAN",
                background_color=(0, 0, 0),
                effects=["tagline_flash", "decode_shadows"]
            ),
        ]

    def get_current_scene(self) -> Scene:
        """Get the current scene"""
        if self.current_scene_index < len(self.scenes):
            return self.scenes[self.current_scene_index]
        return self.scenes[-1]

    def update(self, dt: float) -> bool:
        """Update scene timer. Returns True if scene changed."""
        self.scene_timer += dt
        self.total_time += dt
        
        current_scene = self.get_current_scene()
        if self.scene_timer >= current_scene.duration:
            self.scene_timer = 0
            self.current_scene_index += 1
            return True
        return False

    def is_finished(self) -> bool:
        """Check if presentation is finished"""
        return self.current_scene_index >= len(self.scenes)

# ============================================================================
# HELLO WORLD VIDEO PRESENTATION
# ============================================================================

class TacticalLegendsPresentation:
    """Main presentation class"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tactical Legends: Rise of OISTARIAN - Video Presentation")
        self.clock = pygame.time.Clock()
        
        self.scene_manager = SceneManager()
        self.text_renderer = TextRenderer(self.screen)
        self.particles: List[ParticleEffect] = []
        self.neon_flashes: List[NeonFlash] = []
        self.glitch_effect = GlitchEffect()
        
        self.running = True
        
        # Print "Hello World"
        print("=" * 80)
        print("TACTICAL LEGENDS - RISE OF OISTARIAN")
        print("Video Presentation Generator")
        print("=" * 80)
        print("Hello World! Starting presentation...")
        print("=" * 80)

    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Skip to next scene
                    self.scene_manager.current_scene_index += 1
                    self.scene_manager.scene_timer = 0

    def update(self, dt: float):
        """Update presentation logic"""
        # Update scene timing
        scene_changed = self.scene_manager.update(dt)
        if scene_changed:
            print(f"Scene Changed: {self.scene_manager.get_current_scene().name}")
        
        # Update effects
        self.glitch_effect.update(dt)
        
        # Update particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update(dt)
        
        # Update neon flashes
        self.neon_flashes = [n for n in self.neon_flashes if n.is_active()]
        for flash in self.neon_flashes:
            flash.update(dt)
        
        # Add random particles for effect
        if len(self.particles) < 50:
            import random
            self.particles.append(ParticleEffect(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                (0, 255, 255) if random.random() > 0.5 else (255, 100, 0),
                random.uniform(0.5, 2.0)
            ))

    def render(self):
        """Render the presentation"""
        scene = self.scene_manager.get_current_scene()
        
        # Fill background
        self.screen.fill(scene.background_color)
        
        # Render particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Calculate text opacity based on scene progress
        progress = self.scene_manager.scene_timer / scene.duration
        opacity = min(1.0, progress * 2)  # Fade in
        if progress > 0.8:
            opacity = max(0, (1 - progress) * 5)  # Fade out
        
        # Render narration text
        narration_surface = self.text_renderer.render_narration(
            scene.narration_text,
            opacity=opacity
        )
        self.text_renderer.render_centered(self.screen, narration_surface, y_offset=-200)
        
        # Render tagline for final scene
        if scene.scene_type == SceneType.CREDITS:
            tagline = self.text_renderer.render_tagline("Decode the shadows. Unleash the legend.")
            self.text_renderer.render_centered(self.screen, tagline, y_offset=100)
        
        # Render neon flashes
        for flash in self.neon_flashes:
            if flash.is_active():
                flash_color = flash.get_overlay_color()
                flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                flash_surface.fill((0, 255, 255))
                flash_surface.set_alpha(int(flash_color[3]))
                self.screen.blit(flash_surface, (0, 0))
        
        # Render FPS and scene info
        fps_text = self.text_renderer.fonts['subtitle'].render(
            f"FPS: {int(self.clock.get_fps())} | Scene: {self.scene_manager.current_scene_index + 1}/{len(self.scene_manager.scenes)}",
            True,
            (100, 100, 100)
        )
        self.screen.blit(fps_text, (20, 20))
        
        pygame.display.flip()

    def run(self):
        """Main presentation loop"""
        print("\nPresentation Starting...")
        print("Press SPACE to skip scenes, ESC to exit")
        print("-" * 80)
        
        while self.running and not self.scene_manager.is_finished():
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        print("-" * 80)
        print("Presentation Finished!")
        print("=" * 80)
        pygame.quit()
        sys.exit()

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("  ████████╗ █████╗  ██████╗████████╗██╗ ██████╗ █████╗ ██╗     ")
    print("  ╚══██╔══╝██╔══██╗██╔════╝╚══██╔══╝██║██╔════╝██╔══██╗██║     ")
    print("     ██║   ███████║██║        ██║   ██║██║     ███████║██║     ")
    print("     ██║   ██╔══██║██║        ██║   ██║██║     ██╔══██║██║     ")
    print("     ██║   ██║  ██║╚██████╗   ██║   ██║╚██████╗██║  ██║███████╗")
    print("     ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝")
    print("           LEGENDS - RISE OF OISTARIAN")
    print("\n")
    
    presentation = TacticalLegendsPresentation()
    presentation.run()
