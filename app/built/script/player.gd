# res://scripts/player.gd
extends CharacterBody3D

@export var walk_speed := 5.0
@export var sprint_speed := 9.0
@export var gravity := 9.8
@export var mouse_sensitivity := 0.0025

var velocity := Vector3.ZERO
var current_speed := walk_speed

# Interaction
@onready var ray = $RayCast3D
@onready var tooltip = get_node("/root/MainUI/Tooltip") # adjust path to your Tooltip node
@onready var tutorial = get_node("/root/MainUI/TutorialTooltip")

# State machine for onboarding steps
enum OnboardStep { STEP_MOVE, STEP_INTERACT, STEP_COMBAT, STEP_ABILITY, STEP_PUZZLE, STEP_SAVE }
var step := OnboardStep.STEP_MOVE
var has_moved := false
var has_interacted := false
var has_completed_puzzle := false
var resource_collected := false

func _ready():
    Input.set_mouse_mode(Input.MouseMode.GRABBED)
    _show_hint_for_current_step()

func _process(_delta):
    _update_tooltip_visibility()

func _physics_process(delta):
    _handle_mMovement(delta)
    _check_onboard_progress()

func _handle_mMovement(delta):
    var input_dir = Vector3.ZERO
    input_dir.z = Input.get_action_strength("ui_move_backward") - Input.get_action_strength("ui_move_forward")
    input_dir.x = Input.get_action_strength("ui_move_right") - Input.get_action_strength("ui_move_left")
    input_dir = input_dir.normalized()

    var cam_basis = global_transform.basis
    var forward = -cam_basis.z
    var right = cam_basis.x

    var dir = (forward * input_dir.z) + (right * input_dir.x)
    dir = dir.normalized()

    current_speed = walk_speed
    if Input.is_action_pressed("sprint"):
        current_speed = sprint_speed

    velocity.x = dir.x * current_speed
    velocity.z = dir.z * current_speed
    velocity.y -= gravity * delta
    velocity = move_and_slide(velocity, Vector3.UP)

    if dir.length() > 0.1:
        has_moved = true

func _unhandled_input(event):
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * mouse_sensitivity)
        $Camera3D.rotate_x(-event.relative.y * mouse_sensitivity)

    if event is InputEventKey and event. pressed and event.scancode == KEY_ESCAPE:
        get_tree().paused = not get_tree().paused

func _on_interaction():
    # Called by interactable objects when they are activated
    has_interacted = true
    _update_step_after_interact()

func _update_step_after_interact():
    if step == OnboardStep.STEP_MOVE and has_moved:
        step = OnboardStep.STEP_INTERACT
        _show_hint_for_current_step()

func _on_puzzle_solved():
    has_completed_puzzle = true
    if step == OnboardStep.STEP_PUZZLE:
        step = OnboardStep.STEP_SAVE
        _show_hint_for_current_step()

func _update_tooltip_visibility():
    # Generic logic to hide/show the tooltip based on the step
    match step:
        OnboardStep.STEP_MOVE:
            tooltip.text = "Use WASD to move. Use your mouse to look around."
        OnboardStep.STEP_INTERACT:
            tooltip.text = "Approach objects and press E to interact."
        OnboardStep.STEP_COMBAT:
            tooltip.text = "Left-click to attack. Right-click to block/dodge."
        OnboardStep.STEP_ABILITY:
            tooltip.text = "Collect resources to unlock your first ability."
        OnboardStep.STEP_PUZZLE:
            tooltip.text = "Solve the puzzle to reveal the path."
        OnboardStep.STEP_SAVE:
            tooltip.text = "Press Esc to pause and save progress."
        _:
            tooltip.visible = false

func _show_hint_for_current_step():
    match step:
        OnboardStep.STEP_MOVE:
            tutorial.call("show_step", "Move with WASD and look with the mouse.")
        OnboardStep.STEP_INTERACT:
            tutorial.call("show_step", "Interact with nearby objects using E.")
        OnboardStep.STEP_COMBAT:
            tutorial.call("show_step", "Fight: Attack with LMB, Dodge with RMB.")
        OnboardStep.STEP_ABILITY:
            tutorial.call("show_step", "Collect a crystal to unlock a new ability.")
        OnboardStep.STEP_PUZZLE:
            tutorial.call("show_step", "Solve the platform puzzle to proceed.")
        OnboardStep.STEP_SAVE:
            tutorial.call("show_step", "Pause (Esc) to save and manage progress.")
        _:
            pass


Proposed fictional setting and tone

Setting: The archipelago nation of Imeria, a federation of islands with competing factions, deep-sea routes, and contested resource nodes.
Tone: Cinematic thriller with political intrigue and moral ambiguity. Gritty but respectful, focusing on decisions, consequences, and the human cost of war.
Core themes: miscommunication vs. intelligence, leadership under pressure, the ethics of preemptive action, alliance diplomacy, and civilian impact.
Outline of deliverables you’ll receive in a single, cohesive package

Screenplay: scene-by-scene, dialogue-ready script
Scene 1: Prologue in the Royal Map Room
Beats: Introduce protagonist (codename “Haakon”), mentor/reference figure, and stakes. A crisis triggers the first tactical decision.
Dialogue samples include: briefing, tension around intel gaps, and a moral choice presented to the player.
Scene 2: First Contact – Oceanic Patrol
Beats: Ambiguous threat detected; decision branches lead to different tactical stances (defensive, punitive, or diplomatic).
Dialogue samples reflect political nuance and potential consequences.
Scene 3: Island City Gate – Civilian Corridor
Beats: Civilian evacuation vs. securing strategic assets; outcomes affect civilian welfare metrics in-game.
Scene 4: The Temple of Echoes – Puzzle/Intel Interlude
Beats: A symbolic puzzle representing “matching signals to intent”; player uncovers layered backstory about factions.
Scene 5: The Iron Reef – Surface Battle
Beats: Real-time/turn-based hybrid combat sequence with ethical choices (collateral risk, rescue ops).
Scene 6: Summit at Dusk – Diplomatic Consequences
Beats: Player choices influence who attends the treaty; multiple endings based on risk assessment, empathy, and strategic leanings.
Epilogue: Aftermath and Rise of Narrative Arcs
Several short vignettes show long-term outcomes in Imeria’s world, with a clear note on fictionalization and educational framing.
Godot implementation plan (structure and data-driven design)
Project structure (Godot 4)

Scenes/
01_Prologue.tscn
02_OceanContact.tscn
03_IslandGate.tscn
04_TempleEchoes.tscn
05_IronReef.tscn
06_Summit.tscn
ui/
CinematicHUD.tscn
Subtitles.tscn
ChoicePanel.tscn
WarningsOverlay.tscn
scripts/
cinematic_manager.gd
dialogue_system.gd
tactical_controller.gd
ethics_tracker.gd
education_overlay.gd
assets/
characters/
environments/
audio/
project.godot (Godot 4)
Cinematic pipeline

Cinematic scenes as cutscenes with camera cues, VO lines, and subtitles.
A dialogue system that supports branching based on player choices (DecisionTree).
Event triggers to switch to tactical gameplay nodes (cover, line-of-sight, abilities).
Audio cues: ambient, combat SFX, voiceover, and non-diegetic score.
