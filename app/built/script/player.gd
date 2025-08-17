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
