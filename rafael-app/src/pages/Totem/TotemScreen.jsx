import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { X } from "lucide-react";
import { Link } from "react-router-dom";

const STATES = [
  { id: "standby", label: "STANDBY", color: "#0439D9" },
  { id: "ouvindo", label: "OUVINDO", color: "#5086F2" },
  { id: "pensando", label: "PENSANDO", color: "#9E99BF" },
  { id: "falando", label: "FALANDO", color: "#386273" },
  { id: "alerta", label: "ALERTA", color: "#A64141" },
];

const API_URL = "http://localhost:8000";

export function TotemScreen() {
  const [rafaelState, setRafaelState] = useState("standby");
  const [resposta, setResposta] = useState("");
  
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  // Mock de sessão
  const idoso_id = 1;
  const sessao_id = 1;

  async function iniciarGravacao() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
      chunksRef.current = [];

      recorder.ondataavailable = (e) => chunksRef.current.push(e.data);
      recorder.onstop = enviarAudio;

      recorder.start();
      mediaRecorderRef.current = recorder;
      setRafaelState("ouvindo");
    } catch (err) {
      console.error("Erro ao acessar microfone", err);
      alert("Precisamos de acesso ao seu microfone para conversar!");
    }
  }

  function pararGravacao() {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setRafaelState("pensando");
    }
  }

  async function enviarAudio() {
    const blob = new Blob(chunksRef.current, { type: "audio/webm" });
    const form = new FormData();
    form.append("audio", blob, "audio.webm");
    form.append("idoso_id", idoso_id);
    form.append("sessao_id", sessao_id);

    try {
      const res = await fetch(`${API_URL}/falar`, { method: "POST", body: form });
      const data = await res.json();

      setResposta(data.resposta);
      
      if (data.resposta) {
        setRafaelState("falando");
        const utterance = new SpeechSynthesisUtterance(data.resposta);
        utterance.lang = "pt-BR";
        utterance.onend = () => {
          setRafaelState("standby");
        };
        speechSynthesis.speak(utterance);
      } else {
         setRafaelState("standby");
      }
    } catch (err) {
      console.error("Erro ao enviar áudio", err);
      setRafaelState("standby");
    }
  }

  const currentStateDef = STATES.find(s => s.id === rafaelState);
  const activeColor = currentStateDef.color;

  const isSpeaking = rafaelState === "falando";
  const isListening = rafaelState === "ouvindo";

  return (
    <div className="flex flex-col items-center min-h-screen bg-[#FEFDF9] relative overflow-hidden font-sans select-none">
      
      <div className="absolute top-8 right-8 text-[#DDDCF2] hover:text-[#9E99BF] transition-colors z-50">
        <Link to="/">
          <X className="w-8 h-8" />
        </Link>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center w-full max-w-md mx-auto px-6">
        
        {/* Esfera interativa. Agora serve de botão (Walkie-Talkie). */}
        <div 
          className="relative flex items-center justify-center w-[320px] h-[320px] mb-10 cursor-pointer"
          onMouseDown={iniciarGravacao}
          onMouseUp={pararGravacao}
          onMouseLeave={pararGravacao} /* Se o dedo escapar, para de gravar */
          onTouchStart={iniciarGravacao}
          onTouchEnd={pararGravacao}
        >
          
          {(isListening || isSpeaking) && (
            <motion.div
              className="absolute w-full h-full rounded-full opacity-10"
              style={{ backgroundColor: activeColor }}
              initial={{ scale: 1 }}
              animate={{ scale: isSpeaking ? [1, 1.3, 1] : [1, 1.15, 1] }}
              transition={{
                repeat: Infinity,
                duration: isSpeaking ? 0.8 : 2,
                ease: "easeInOut",
              }}
            />
          )}

          {isSpeaking && (
            <motion.div
              className="absolute w-full h-full rounded-full opacity-5"
              style={{ backgroundColor: activeColor }}
              initial={{ scale: 1 }}
              animate={{ scale: [1, 1.5, 1] }}
              transition={{
                repeat: Infinity,
                duration: 1.2,
                ease: "easeInOut",
                delay: 0.2
              }}
            />
          )}

          <motion.div
            className="relative w-[280px] h-[280px] rounded-full flex items-center justify-center text-center"
            style={{ 
              background: `radial-gradient(circle at 35% 25%, #5086F2 0%, ${activeColor} 40%, #011140 100%)`,
              boxShadow: `0 20px 40px -10px ${activeColor}40`
            }}
            animate={{
              scale: rafaelState === "pensando" ? [1, 0.95, 1] : 
                     rafaelState === "alerta" ? [1, 1.05, 1] : 1,
            }}
            transition={{
              repeat: Infinity,
              duration: rafaelState === "alerta" ? 0.5 : 3,
              ease: "easeInOut",
            }}
          >
            {/* Texto auxiliar dentro da esfera caso queira */}
            <span className="text-white/60 font-medium z-10 pointer-events-none drop-shadow-md px-4">
              {rafaelState === "standby" ? "Toque e Segure\\npara falar" : 
               rafaelState === "ouvindo" ? "Pode falar..." : 
               rafaelState === "pensando" ? "Pensando..." : ""}
            </span>
            <div className="absolute inset-0 rounded-full w-full h-full bg-gradient-to-tr from-white/0 to-white/20 mix-blend-overlay"></div>
          </motion.div>
        </div>

        <div className="text-center w-full mb-8">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-[#352F59] mb-4">
            Estou aqui com<br/>você, <span className="text-[#0439D9]">Seu</span><br/><span className="text-[#0439D9]">João</span>.
          </h1>
          <p className="text-[#9E99BF] font-medium text-lg px-8 min-h-[60px]">
            {resposta ? resposta : "Pode falar comigo a qualquer momento."}
          </p>
        </div>
      </div>

    </div>
  );
}
