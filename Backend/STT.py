# Backend/STT.py
import io
import soundfile as sf
from faster_whisper import WhisperModel

# Carrega o modelo uma vez na inicialização (não a cada chamada)
# model_size: "tiny" (mais rápido) | "base" | "small" (melhor custo-benefício)
print("Carregando modelo Whisper...")
_model = WhisperModel("small", device="cpu", compute_type="int8")
print("Whisper carregado.")

def transcrever(audio_bytes: bytes, formato: str = "webm") -> str:
    """
    Recebe bytes de áudio brutos e retorna o texto transcrito em pt-BR.
    Aceita qualquer formato que o soundfile suporte (wav, webm, ogg, mp3).
    """
    try:
        # Converte bytes -> array numpy que o Whisper entende
        audio_buffer = io.BytesIO(audio_bytes)
        audio_array, sample_rate = sf.read(audio_buffer, dtype="float32")

        # Se estéreo, converte para mono
        if audio_array.ndim > 1:
            audio_array = audio_array.mean(axis=1)

        # Transcreve
        segments, info = _model.transcribe(
            audio_array,
            language="pt",
            beam_size=5,
            vad_filter=True,           # ignora silêncio automaticamente
            vad_parameters=dict(
                min_silence_duration_ms=500  # pausa mínima para cortar
            )
        )

        texto = " ".join(seg.text.strip() for seg in segments)
        return texto.strip()
    except Exception as e:
        print(f"Erro no STT: {e}")
        return ""
