from typing import Dict

# Basic localized translations for core UI alerts (greetings, emergency warnings)
LOCAL_DICTIONARY = {
    "spanish": {
        "emergency_alert": "ALERTA DE EMERGENCIA: Busque atención médica de inmediato. Llame al 911.",
        "chest_pain_instruction": "Si siente dolor de pecho, no conduzca solo. Llame a una ambulancia.",
        "medication_reminder": "Recordatorio de medicamento: Tome su dosis a tiempo.",
        "welcome": "Bienvenido a LifeBridge AI. Su navegador de salud autónomo."
    },
    "hindi": {
        "emergency_alert": "आपातकालीन चेतावनी: तुरंत चिकित्सा सहायता लें। 112 या 102 पर कॉल करें।",
        "chest_pain_instruction": "यदि सीने में दर्द है, तो स्वयं वाहन न चलाएं। एम्बुलेंस बुलाएं।",
        "medication_reminder": "दवा अनुस्मारक: अपनी खुराक समय पर लें।",
        "welcome": "लाइफब्रिज एआई में आपका स्वागत है। आपका स्वायत्त स्वास्थ्य सहायक।"
    },
    "swahili": {
        "emergency_alert": "TAHADHARI YA DHARURA: Tafuta usaidizi wa matibabu mara moja. Piga simu 112 au 999.",
        "chest_pain_instruction": "Ikiwa una maumivu ya kifua, usiendeshe gari peke yako. Piga simu gari la wagonjwa.",
        "medication_reminder": "Kikumbusho cha dawa: Chukua dozi yako kwa wakati.",
        "welcome": "Karibu kwenye LifeBridge AI. Kiongozi wako wa afya anayejitegemea."
    }
}

class TranslationTool:
    """
    Translates response outputs and summaries to local languages to support global health equity.
    """
    def translate(self, text: str, target_lang: str) -> str:
        lang = target_lang.lower().strip()
        
        # Check dictionary for exact keys
        if lang in LOCAL_DICTIONARY:
            for k, val in LOCAL_DICTIONARY[lang].items():
                if k in text.lower():
                    return val
                    
        # Simple suffix translation simulation (or we can use Gemini in the Orchestrator for full paragraphs)
        if lang == "spanish":
            return f"[Traducción al Español]: {text}"
        elif lang == "hindi":
            return f"[हिंदी अनुवाद]: {text}"
        elif lang == "swahili":
            return f"[Tafsiri ya Kiswahili]: {text}"
            
        return text
