import React from "react";
import { Link } from "react-router-dom";
import { Battery, Eye, Smile, Pill, Church, Mic, MapPin, Sparkles, LayoutGrid, Settings, Target, Menu } from "lucide-react";
import { Button } from "../../components/ui/Button";

export function DashboardScreen() {
  return (
    <div className="min-h-screen bg-[#F8F9FC] font-sans text-[#0D0D0D] flex justify-center pb-24">
      {/* Container imitando aspecto Mobile em telas maiores */}
      <div className="w-full max-w-md bg-white min-h-screen relative shadow-sm">
        
        {/* Navbar */}
        <nav className="flex items-center justify-between px-6 py-5 bg-white">
          <div className="flex items-center gap-4">
            <Menu className="w-6 h-6 text-[#0439D9]" />
            <h1 className="text-xl font-bold text-[#0439D9]">Rafael</h1>
          </div>
          {/* Avatar Dummy */}
          <div className="w-9 h-9 rounded-full bg-slate-300 overflow-hidden shadow-sm shrink-0 border border-slate-100">
            <img src={`https://api.dicebear.com/7.x/notionists/svg?seed=Isaac&backgroundColor=e2e8f0`} alt="Avatar" className="w-full h-full object-cover" />
          </div>
        </nav>

        <main className="px-6 space-y-6">
          
          {/* Banner Principal */}
          <section className="bg-[#EBEAF5] rounded-3xl p-6 relative overflow-hidden">
            <h2 className="text-2xl font-bold text-[#0439D9] leading-tight mb-6 mt-2 max-w-[200px]">
              O Seu João está tranquilo e seguro hoje.
            </h2>
            <div className="flex flex-col items-start gap-3">
              <div className="flex items-center bg-white px-4 py-2 rounded-full text-[13px] font-bold text-[#352F59] shadow-sm">
                <Battery className="w-4 h-4 mr-2 text-green-500 stroke-[3]" /> Bateria: 85%
              </div>
              <div className="flex items-center bg-white px-4 py-2 rounded-full text-[13px] font-bold text-[#352F59] shadow-sm">
                <Eye className="w-4 h-4 mr-2 text-[#0439D9] stroke-[3]" /> Visto por último: 15 min
              </div>
            </div>
          </section>

          {/* Diário Emocional */}
          <section>
            <div className="flex justify-between items-center mb-5 mt-8 max-w-xs">
              <h3 className="text-lg font-bold">Diário Emocional</h3>
              <span className="text-[10px] text-gray-400 font-bold tracking-widest">HOJE</span>
            </div>

            <div className="space-y-4">
              {/* Timeline Item 1 */}
              <div className="bg-white rounded-3xl p-5 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.05)] border border-gray-50 flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-8 h-8 rounded-full bg-[#E5F5EC] flex items-center justify-center shrink-0">
                    <Smile className="w-5 h-5 text-green-600" />
                  </div>
                  {/* Linha vertical */}
                  <div className="w-px h-full bg-gray-200 mt-2"></div>
                </div>
                <div>
                  <div className="text-[11px] font-bold text-gray-400 mb-0.5">10:15</div>
                  <h4 className="font-bold text-sm text-[#0D0D0D]">Happy memories</h4>
                  <p className="text-sm text-gray-500 mt-1 leading-relaxed">
                    Compartilhou histórias sobre a infância no interior com o assistente.
                  </p>
                </div>
              </div>

              {/* Timeline Item 2 */}
              <div className="bg-white rounded-3xl p-5 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.05)] border border-gray-50 flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-8 h-8 rounded-full bg-[#E5ECF6] flex items-center justify-center shrink-0">
                    <Pill className="w-4 h-4 text-blue-500" />
                  </div>
                  <div className="w-px h-full bg-gray-200 mt-2"></div>
                </div>
                <div>
                  <div className="text-[11px] font-bold text-gray-400 mb-0.5">13:30</div>
                  <h4 className="font-bold text-sm text-[#0D0D0D]">Medication taken</h4>
                  <p className="text-sm text-gray-500 mt-1 leading-relaxed">
                    Confirmou a ingestão do medicamento de uso contínuo do meio-dia.
                  </p>
                </div>
              </div>

              {/* Timeline Item 3 */}
              <div className="bg-white rounded-3xl p-5 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.05)] border border-gray-50 flex gap-4">
                <div className="flex flex-col items-center relative">
                  <div className="w-8 h-8 rounded-full bg-[#F0F2F9] flex items-center justify-center shrink-0">
                    <Church className="w-4 h-4 text-[#352F59]" />
                  </div>
                </div>
                <div className="pb-2">
                  <div className="text-[11px] font-bold text-gray-400 mb-0.5">16:00</div>
                  <h4 className="font-bold text-sm text-[#0D0D0D]">Spiritual moment</h4>
                  <p className="text-sm text-gray-500 mt-1 leading-relaxed">
                    Ouviu hinos e realizou momento de oração programado.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Gráfico */}
          <section className="bg-white rounded-3xl p-6 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.05)] border border-gray-50 mt-6 relative">
            <div className="absolute right-6 top-6">
              <span className="text-2xl font-bold text-[#0439D9]">+12%</span>
            </div>
            <h3 className="font-bold text-lg leading-tight">Nível de Conversa</h3>
            <p className="text-xs text-gray-500 mb-8 mt-1">Engajamento verbal diário</p>
            
            <div className="flex items-end justify-between h-28 px-2 space-x-2">
              <div className="flex flex-col items-center flex-1 gap-2">
                <div className="w-full bg-[#F2F2F2] rounded-full h-10"></div>
                <span className="text-[9px] text-gray-400 font-bold uppercase tracking-widest">SEG</span>
              </div>
              <div className="flex flex-col items-center flex-1 gap-2">
                <div className="w-full bg-[#F2F2F2] rounded-full h-14"></div>
                <span className="text-[9px] text-gray-400 font-bold uppercase tracking-widest">TER</span>
              </div>
              <div className="flex flex-col items-center flex-1 gap-2">
                <div className="w-full bg-[#F2F2F2] rounded-full h-12"></div>
                <span className="text-[9px] text-gray-400 font-bold uppercase tracking-widest">QUA</span>
              </div>
              <div className="flex flex-col items-center flex-1 gap-2">
                <div className="w-full bg-[#F2F2F2] rounded-full h-16"></div>
                <span className="text-[9px] text-gray-400 font-bold uppercase tracking-widest">QUI</span>
              </div>
              <div className="flex flex-col items-center flex-1 gap-2">
                <div className="w-full bg-[#0439D9] rounded-full h-24"></div>
                <span className="text-[9px] text-[#0439D9] font-bold uppercase tracking-widest">HOJE</span>
              </div>
            </div>
          </section>

          {/* Ações */}
          <section className="mt-8 space-y-4">
            <h3 className="text-lg font-bold mb-3">Ações</h3>
            <button className="w-full bg-white border-2 border-[#0439D9] text-[#0439D9] font-bold rounded-full py-4 flex items-center justify-center gap-2 hover:bg-[#F2F2F2] transition-colors">
              <Mic className="w-5 h-5" /> Mandar mensagem de voz
            </button>
            <button className="w-full bg-[#b23b3b] text-white font-bold rounded-full py-4 flex items-center justify-center gap-2 shadow-md hover:bg-red-800 transition-colors">
              <MapPin className="w-5 h-5" /> Acionar Ligação de Emergência
            </button>
          </section>

          {/* Banner Inferior Informativo */}
          <section className="bg-[#EFEEFA] rounded-2xl p-5 mb-8 flex gap-4 items-center">
            <div className="w-10 h-10 rounded-full bg-[#0439D9] flex items-center justify-center shrink-0">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <p className="text-[13px] text-gray-500 font-medium leading-relaxed pr-2">
              O assistente está monitorando as atividades e o bem-estar emocional em tempo real.
            </p>
          </section>

        </main>

        {/* Bottom Navigation Navbar */}
        <div className="fixed bottom-6 left-0 right-0 flex justify-center z-50">
          <div className="bg-white shadow-[0_10px_40px_-10px_rgba(0,0,0,0.15)] border border-gray-100 rounded-full px-6 py-3 flex items-center gap-2">
            
            <Link to="/totem" className="flex flex-col items-center justify-center w-16 h-12 text-gray-400 hover:text-gray-800 transition-colors">
              <Target className="w-6 h-6 mb-1 stroke-[2.5]" />
              <span className="text-[10px] font-bold">Totem</span>
            </Link>

            <button className="flex flex-col items-center justify-center w-20 h-12 bg-[#0439D9] text-white rounded-full shadow-lg transform -translate-y-1">
              <LayoutGrid className="w-5 h-5 mb-1 stroke-[2.5]" />
              <span className="text-[10px] font-bold">Painel</span>
            </button>

            <button className="flex flex-col items-center justify-center w-16 h-12 text-gray-400 hover:text-gray-800 transition-colors">
              <Settings className="w-6 h-6 mb-1 stroke-[2.5]" />
              <span className="text-[10px] font-bold">Ajustes</span>
            </button>

          </div>
        </div>

      </div>
    </div>
  );
}
