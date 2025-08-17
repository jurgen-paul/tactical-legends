extends Node

# --- Master Volume Controls ---
@export var master_volume: float = 1.0
@export var sfx_volume: float = 0.8
@export var ambient_volume: float = 0.6

# --- Core Clips ---
@export var menu_select: AudioStream
@export var menu_encrypted_tone: AudioStream
@export var hud_ping: AudioStream
@export var dialogue_fade_in: AudioStream
@export var mission_intro_echo: AudioStream
@export var mutator_warp: AudioStream
@export var stealth_reverb_pulse: AudioStream
@export var pitch_distort_cue: AudioStream

# --- Sources ---
var sfx_player: AudioStreamPlayer
var ambient_player: AudioStreamPlayer
var dialogue_player: AudioStreamPlayer

# --- Ambient Cache ---
var ambient_clip_cache: = {}
var current_ambient_mood: String = ""

func _ready():
    _initialize_audio_players()
    play_ambient_loop("CalmAtmosphere")

func _initialize_audio_players():
    sfx_player = AudioStreamPlayer.new()
    add_child(sfx_player)
    sfx_player.volume_db = linear2db(sfx_volume)

    ambient_player = AudioStreamPlayer.new()
    add_child(ambient_player)
    ambient_player.volume_db = linear2db(ambient_volume)
    ambient_player.bus = "Ambient"
    ambient_player.stream_paused = false
    ambient_player.autoplay = false

    dialogue_player = AudioStreamPlayer.new()
    add_child(dialogue_player)
    dialogue_player.bus = "Dialogue"
    dialogue_player.volume_db = linear2db(1.0)

# --- Menu Interaction Sounds ---
func play_menu_select():
    if menu_select:
        sfx_player.stream = menu_select
        sfx_player.pitch_scale = 1.0
        sfx_player.play()

func play_encrypted_tone():
    if menu_encrypted_tone:
        sfx_player.stream = menu_encrypted_tone
        sfx_player.pitch_scale = 1.2
        sfx_player.play()
        yield(get_tree().create_timer(menu_encrypted_tone.get_length()), "timeout")
        sfx_player.pitch_scale = 1.0

# --- HUD Feedback (Echo & Ping) ---
func trigger_hud_ping():
    if hud_ping:
        sfx_player.stream = hud_ping
        sfx_player.pitch_scale = 1.0
        sfx_player.play()
        # Simulate echo with short delay replay
        yield(get_tree().create_timer(0.15), "timeout")
        sfx_player.play()

# --- Dialogue FX ---
func play_dialogue_intro(clip: AudioStream):
    if clip == null:
        return
    dialogue_player.stream = dialogue_fade_in if dialogue_fade_in else clip
    dialogue_player.play()
    yield(get_tree().create_timer(0.5), "timeout")
    dialogue_player.stream = clip
    dialogue_player.play()

# --- Mutator FX ---
func trigger_mutator_effect(effect_type: String):
    var t = effect_type.to_lower()
    if t == "gravityreversal":
        _gravity_reversal_effect()
    elif t == "invisiblemovement":
        _apply_pitch_distortion()
    elif t == "timedilation":
        _time_dilation_effect()
    else:
        push_warning("Unknown mutator effect: %s" % effect_type)

func _gravity_reversal_effect():
    sfx_player.pitch_scale = 0.5
    if mutator_warp:
        sfx_player.stream = mutator_warp
        sfx_player.play()
    yield(get_tree().create_timer(2.0), "timeout")
    sfx_player.pitch_scale = 1.0

func _time_dilation_effect():
    var original_pitch = ambient_player.pitch_scale
    ambient_player.pitch_scale = 0.7
    yield(get_tree().create_timer(3.0), "timeout")
    # Smooth transition back
    var start = ambient_player.pitch_scale
    var elapsed = 0.0
    var duration = 1.0
    while elapsed < duration:
        elapsed += get_process_delta_time()
        ambient_player.pitch_scale = lerp(start, original_pitch, elapsed / duration)
        yield(get_tree(), "idle_frame")
    ambient_player.pitch_scale = original_pitch

func _apply_pitch_distortion():
    sfx_player.pitch_scale = 0.6
    if pitch_distort_cue:
        sfx_player.stream = pitch_distort_cue
        sfx_player.play()
    yield(get_tree().create_timer(1.0), "timeout")
    sfx_player.pitch_scale = 1.0

# --- Stealth Reverb Pulse ---
func trigger_stealth_pulse():
    if stealth_reverb_pulse:
        sfx_player.stream = stealth_reverb_pulse
        sfx_player.play()
        # You can simulate reverb with a short delay replay, or use Godot's bus effect
        yield(get_tree().create_timer(1.5), "timeout")

# --- Ambient Layer Control ---
func play_ambient_loop(mood: String):
    if current_ambient_mood == mood:
        return
    var clip = _get_ambient_clip(mood)
    if clip == null:
        return
    _crossfade_ambient(clip, mood)

func _crossfade_ambient(new_clip: AudioStream, mood: String):
    var fade_time = 1.0
    var original_volume = db2linear(ambient_player.volume_db)
    # Fade out
    var elapsed = 0.0
    while elapsed < fade_time:
        elapsed += get_process_delta_time()
        ambient_player.volume_db = linear2db(lerp(original_volume, 0.0, elapsed / fade_time))
        yield(get_tree(), "idle_frame")
    # Switch
    ambient_player.stream = new_clip
    ambient_player.play()
    current_ambient_mood = mood
    # Fade in
    elapsed = 0.0
    while elapsed < fade_time:
        elapsed += get_process_delta_time()
        ambient_player.volume_db = linear2db(lerp(0.0, ambient_volume, elapsed / fade_time))
        yield(get_tree(), "idle_frame")
    ambient_player.volume_db = linear2db(ambient_volume)

func _get_ambient_clip(mood: String) -> AudioStream:
    if ambient_clip_cache.has(mood):
        return ambient_clip_cache[mood]
    var path = "res://Audio/Ambient/%s.ogg" % mood
    var clip = load(path)
    if clip:
        ambient_clip_cache[mood] = clip
    else:
        push_warning("Ambient clip not found: %s" % path)
    return clip

# --- Volume Controls ---
func set_master_volume(vol: float):
    master_volume = clamp(vol, 0.0, 1.0)
    AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Master"), linear2db(master_volume))

func set_sfx_volume(vol: float):
    sfx_volume = clamp(vol, 0.0, 1.0)
    sfx_player.volume_db = linear2db(sfx_volume)

func set_ambient_volume(vol: float):
    ambient_volume = clamp(vol, 0.0, 1.0)
    ambient_player.volume_db = linear2db(ambient_volume)

func _exit_tree():
    sfx_player.stop()
    ambient_player.stop()
    dialogue_player.stop()
