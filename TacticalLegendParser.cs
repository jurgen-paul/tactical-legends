using System.Collections.Generic;
using System.Text.RegularExpressions;

public static class TacticalLegendParser
{
    // Define tag mappings
    private static readonly Dictionary<string, string> tagMap = new Dictionary<string, string>
    {
        { "~~echo-wave~~", "<i><color=#00FFFF>EchoWave</color></i>" },
        { "**vault-sigil**", "<b><color=#3366FF>VaultSigil</color></b>" },
        { "//eden-glyph//", "<i><color=#66FF66>EdenGlyph</color></i>" },
        { "--stricken-protocol--", "<s>StrickenProtocol</s>" },
        { "__underlined-command__", "<u>UnderlinedCommand</u>" },
        { "~__unstable-thread__", "<u><color=#FF3333>UnstableThread</color></u>" },
        { "<vb>", "<b><color=#3366FF>" },
        { "<oi>", "<i><color=#FF9900>" },
        { "<ec:mono>", "<font=monospace><color=#66FF66>" },
        { "<strike:green>", "<s><color=green>" },
        { "<underline:red>", "<u><color=red>" },
        { "<wave:#0000FF>", "<i><color=#0000FF>" },
        { "<color:eden-blue>", "<color=#66FFCC>" },
        { "<back:vault-orange>", "<mark=#FFA500>" },
        { "<size:20>", "<size=20>" }
    };

    // Apply formatting to input text
    public static string Parse(string input)
    {
        if (string.IsNullOrEmpty(input))
            return input;

        foreach (var tag in tagMap)
        {
            input = input.Replace(tag.Key, tag.Value);
        }

        // Close any open tags (simplified)
        input = Regex.Replace(input, @"(?<!</)(EchoWave|VaultSigil|EdenGlyph|StrickenProtocol|UnderlinedCommand|UnstableThread)", "$1</color></i></b></u></s>");

        return input;
    }
}

public class TextStyler : MonoBehaviour
{
    public TextMeshProUGUI targetText;

    public void ApplyStyledText(string rawInput)
    {
        if (targetText == null)
        {
            Debug.LogError("TextStyler: targetText is not assigned!");
            return;
        }

        string styled = TacticalLegendParser.Parse(rawInput);
        targetText.text = styled;
    }
}

public class AnimationEngine : MonoBehaviour
{
    public void AnimateTag(string tagType, GameObject target)
    {
        if (target == null)
        {
            Debug.LogError($"AnimationEngine: Target is null for tag '{tagType}'");
            return;
        }

        switch (tagType)
        {
            case "vault-sigil":
                StartCoroutine(GlowEffect(target, Color.blue));
                break;
            case "eden-glyph":
                StartCoroutine(PulseEffect(target, Color.green));
                break;
            case "echo-wave":
                StartCoroutine(WaveEffect(target));
                break;
            default:
                Debug.LogWarning($"AnimationEngine: Unknown tag type '{tagType}'");
                break;
        }
    }

    IEnumerator GlowEffect(GameObject obj, Color glowColor)
    {
        try
        {
            var renderer = obj.GetComponent<MeshRenderer>();
            if (renderer == null) yield break;

            Material mat = renderer.material;
            Color originalColor = mat.color;

            for (float t = 0; t < 1f; t += Time.deltaTime)
            {
                mat.color = Color.Lerp(originalColor, glowColor, t);
                yield return null;
            }

            mat.color = originalColor;
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"GlowEffect error: {ex.Message}");
        }
    }

    IEnumerator PulseEffect(GameObject obj, Color pulseColor)
    {
        try
        {
            var renderer = obj.GetComponent<MeshRenderer>();
            if (renderer == null) yield break;

            Material mat = renderer.material;
            Color originalColor = mat.color;

            for (int i = 0; i < 3; i++)
            {
                for (float t = 0; t < 1f; t += Time.deltaTime * 2)
                {
                    mat.color = Color.Lerp(originalColor, pulseColor, t);
                    yield return null;
                }

                for (float t = 0; t < 1f; t += Time.deltaTime * 2)
                {
                    mat.color = Color.Lerp(pulseColor, originalColor, t);
                    yield return null;
                }
            }

            mat.color = originalColor;
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"PulseEffect error: {ex.Message}");
        }
    }

    IEnumerator WaveEffect(GameObject obj)
    {
        try
        {
            var meshFilter = obj.GetComponent<MeshFilter>();
            if (meshFilter == null) yield break;

            for (float t = 0; t < 1f; t += Time.deltaTime)
            {
                yield return null;
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"WaveEffect error: {ex.Message}");
        }
    }
}

public class VoiceoverManager : MonoBehaviour
{
    public AudioSource audioSource;
    public AudioClip vaultbornClip;
    public AudioClip edenWhisper;
    public AudioClip oistarianAlert;

    public void TriggerVoice(string tagType)
    {
        if (audioSource == null)
        {
            Debug.LogError("VoiceoverManager: audioSource is not assigned!");
            return;
        }

        switch (tagType)
        {
            case "vault-sigil":
                if (vaultbornClip != null)
                    audioSource.PlayOneShot(vaultbornClip);
                break;
            case "eden-glyph":
                if (edenWhisper != null)
                    audioSource.PlayOneShot(edenWhisper);
                break;
            case "oistarian-alert":
                if (oistarianAlert != null)
                    audioSource.PlayOneShot(oistarianAlert);
                break;
            default:
                Debug.LogWarning($"VoiceoverManager: Unknown tag type '{tagType}'");
                break;
        }
    }
}

public class CodexUnlocker : MonoBehaviour
{
    private HashSet<string> unlockedEntries = new HashSet<string>();

    public void UnlockEntry(string entryID)
    {
        if (string.IsNullOrEmpty(entryID))
        {
            Debug.LogWarning("CodexUnlocker: entryID is empty!");
            return;
        }

        if (!unlockedEntries.Contains(entryID))
        {
            unlockedEntries.Add(entryID);
            DisplayCodexEntry(entryID);
        }
    }

    void DisplayCodexEntry(string entryID)
    {
        try
        {
            // Show lore panel, animate reveal, etc.
            Debug.Log($"Codex Entry Unlocked: {entryID}");
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"DisplayCodexEntry error: {ex.Message}");
        }
    }
}

public class UIController : MonoBehaviour
{
    public TextStyler styler;
    public AnimationEngine animator;
    public VoiceoverManager voiceManager;
    public CodexUnlocker codex;

    public void RenderLog(string rawText)
    {
        if (string.IsNullOrEmpty(rawText))
        {
            Debug.LogWarning("UIController: rawText is empty!");
            return;
        }

        if (styler == null || animator == null || voiceManager == null || codex == null)
        {
            Debug.LogError("UIController: One or more required components are not assigned!");
            return;
        }

        try
        {
            styler.ApplyStyledText(rawText);

            foreach (string tag in ExtractTags(rawText))
            {
                animator.AnimateTag(tag, styler.gameObject);
                voiceManager.TriggerVoice(tag);
                codex.UnlockEntry(tag);
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"RenderLog error: {ex.Message}");
        }
    }

    List<string> ExtractTags(string input)
    {
        var tags = new List<string>();
        try
        {
            if (input.Contains("vault-sigil")) tags.Add("vault-sigil");
            if (input.Contains("eden-glyph")) tags.Add("eden-glyph");
            if (input.Contains("echo-wave")) tags.Add("echo-wave");
            if (input.Contains("stricken-protocol")) tags.Add("stricken-protocol");
            if (input.Contains("unstable-thread")) tags.Add("unstable-thread");
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"ExtractTags error: {ex.Message}");
        }

        return tags;
    }
}

public class RelicViewer : MonoBehaviour
{
    public GameObject relicModel;
    public Material vaultbornShader;
    public Material edenShader;
    public Material oistarianShader;

    public void DisplayRelic(RelicData relic)
    {
        if (relic == null)
        {
            Debug.LogError("RelicViewer: relic is null!");
            return;
        }

        if (relicModel == null)
        {
            Debug.LogError("RelicViewer: relicModel is not assigned!");
            return;
        }

        try
        {
            relicModel.GetComponent<MeshRenderer>().material = GetFactionShader(relic.faction);
            relicModel.transform.rotation = Quaternion.identity;
            relicModel.SetActive(true);
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"DisplayRelic error: {ex.Message}");
        }
    }

    private Material GetFactionShader(string faction)
    {
        return faction switch
        {
            "Vaultborn" => vaultbornShader ?? new Material(Shader.Find("Standard")),
            "Eden Core" => edenShader ?? new Material(Shader.Find("Standard")),
            "Oistarian" => oistarianShader ?? new Material(Shader.Find("Standard")),
            _ => vaultbornShader ?? new Material(Shader.Find("Standard"))
        };
    }
}

public class UISkinManager : MonoBehaviour
{
    public UITheme vaultbornTheme;
    public UITheme edenTheme;
    public UITheme oistarianTheme;

    public void ApplyFactionSkin(string faction)
    {
        if (string.IsNullOrEmpty(faction))
        {
            Debug.LogWarning("UISkinManager: faction is empty!");
            faction = "Vaultborn";
        }

        try
        {
            UITheme theme = faction switch
            {
                "Vaultborn" => vaultbornTheme,
                "Eden Core" => edenTheme,
                "Oistarian" => oistarianTheme,
                _ => vaultbornTheme
            };

            if (theme != null)
            {
                UIStyler.ApplyTheme(theme);
                AmbientFXManager.TriggerFactionAmbient(faction);
            }
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"ApplyFactionSkin error: {ex.Message}");
        }
    }
}

public class RelicData
{
    public string name;
    public string faction;
    public string lore;
    public GameObject modelPrefab;
}

public class RelicFusionPreviewer : MonoBehaviour
{
    public GameObject fusionModel;
    public TextMeshProUGUI fusionStats;
    public TextMeshProUGUI fusionLore;

    public void PreviewFusion(Relic relicA, Relic relicB)
    {
        if (relicA == null || relicB == null)
        {
            Debug.LogError("RelicFusionPreviewer: One or both relics are null!");
            return;
        }

        if (fusionModel == null || fusionStats == null || fusionLore == null)
        {
            Debug.LogError("RelicFusionPreviewer: One or more UI components are not assigned!");
            return;
        }

        try
        {
            fusionModel.GetComponent<MeshRenderer>().material = BlendShaders(relicA.faction, relicB.faction);
            fusionStats.text = $"Projected ATK: {(relicA.attack + relicB.attack) / 2 + 10}";
            fusionLore.text = GenerateFusionLore(relicA, relicB);
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"PreviewFusion error: {ex.Message}");
        }
    }

    private Material BlendShaders(string factionA, string factionB)
    {
        return new Material(Shader.Find("Standard"));
    }

    private string GenerateFusionLore(Relic a, Relic b)
    {
        return $"When {a?.name ?? "Unknown"} meets {b?.name ?? "Unknown"}, the vault remembers both. A relic of dual memory emerges.";
    }
}

public class Relic
{
    public string name;
    public string faction;
    public int attack;
    public List<string> traits = new List<string>();
}

public class MissionData
{
    public string name;
    public string environment;
    public bool survived;
    public int difficulty;
    public bool usedWithAllyRelic;
}

public void SimulateEvolution(Relic relic, MissionData mission)
{
    if (relic == null || mission == null)
    {
        Debug.LogError("SimulateEvolution: relic or mission is null!");
        return;
    }

    try
    {
        if (mission.survived && mission.difficulty > 7)
            relic.traits.Add("Endurance Echo");

        if (mission.usedWithAllyRelic)
            relic.traits.Add("Bonded Memory");

        relic.lore += $"Evolved during {mission.name}, adapting to {mission.environment}.";
    }
    catch (System.Exception ex)
    {
        Debug.LogError($"SimulateEvolution error: {ex.Message}");
    }
}
