import React, { useState } from "react";
import { motion } from "framer-motion";
import { X } from "lucide-react";
import { Link } from "react-router-dom";

const STATES = [
  { id: "standby", label: "STANDBY", color: "#0439D9" },
  { id: "ouvindo", label: "OUVINDO", color: "#5086F2" },
  { id: "pensando", label: "PENSANDO", color: "#9E99BF" },
  { id: "falando", label: "FALANDO", color: "#386273" }, // Ou outro tom verde/cyan
  { id: "alerta", label: "ALERTA", color: "#A64141" },
];

export function TotemScreen() {
  const [rafaelState, setRafaelState] = useState("standby");

  const currentStateDef = STATES.find(s => s.id === rafaelState);
  const activeColor = currentStateDef.color;

  const isSpeaking = rafaelState === "falando";
  const isListening = rafaelState === "ouvindo";

  return (
    <div className="flex flex-col items-center min-h-screen bg-[#FEFDF9] relative overflow-hidden font-sans">
      
      {/* Botão Fechar no topo direito (simulando UI da imagem) */}
      <div className="absolute top-8 right-8 text-[#DDDCF2] hover:text-[#9E99BF] transition-colors z-50">
        <Link to="/">
          <X className="w-8 h-8" />
        </Link>
      </div>

      {/* Espaçamento superior */}
      <div className="flex-1 flex flex-col items-center justify-center w-full max-w-md mx-auto px-6">
        
        {/* Container Principal da Esfera */}
        <div className="relative flex items-center justify-center w-[320px] h-[320px] mb-10">
          
          {/* Ripple 1: Escuta e Fala (Framer Motion) */}
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

          {/* Ripple 2: Apenas para "Falando" */}
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

          {/* Esfera Viva Central com Gradiente 3D (Refletindo a imagem ref) */}
          <motion.div
            className="relative w-[280px] h-[280px] rounded-full"
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
            {/* Brilho super sutil interno */}
            <div className="absolute inset-0 rounded-full w-full h-full bg-gradient-to-tr from-white/0 to-white/20 mix-blend-overlay"></div>
          </motion.div>
        </div>

        {/* Textos Centrais (Refletindo imagem ref) */}
        <div className="text-center w-full mb-8">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-[#352F59] mb-4">
            Estou aqui com<br/>você, <span className="text-[#0439D9]">Seu</span><br/><span className="text-[#0439D9]">João</span>.
          </h1>
          <p className="text-[#9E99BF] font-medium text-lg px-8">
            Pode falar comigo a qualquer<br/>momento.
          </p>
        </div>
      </div>

      {/* Painel Inferior de Debug/Troca de Estado (Design idêntico à imagem) */}
      <div className="w-full flex justify-center pb-12 z-50">
        <div className="bg-white/80 backdrop-blur-md shadow-[0_10px_40px_-10px_rgba(0,0,0,0.05)] rounded-full px-8 py-5 flex items-center gap-6 border border-white/50">
          {STATES.map((state) => {
            const isActive = rafaelState === state.id;
            return (
              <button 
                key={state.id}
                onClick={() => setRafaelState(state.id)}
                className="flex flex-col items-center gap-2 transition-all"
              >
                {/* Bolinha do Status */}
                <div 
                  className={`w-5 h-5 rounded-full flex items-center justify-center transition-all ${isActive ? 'scale-110 shadow-sm' : 'opacity-40 hover:opacity-70'}`}
                  style={{ backgroundColor: `${state.color}20` }} /* Fundo bem clarinho */
                >
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: state.color }} 
                  />
                </div>
                {/* Label do Status */}
                <span 
                  className={`text-[10px] font-bold tracking-widest transition-all ${isActive ? 'text-[#011140]' : 'text-[#9E99BF]'}`}
                >
                  {state.label}
                </span>
              </button>
            );
          })}
        </div>
      </div>

    </div>
  );
}
