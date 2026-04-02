import React from "react";
import { cn } from "../../lib/utils";

/**
 * Componente de Botão acessível
 * Mantém no mínimo 48px de altura (acessibilidade motora).
 */
export function Button({ 
  className, 
  variant = "primary", 
  size = "md", 
  children, 
  ...props 
}) {
  const baseStyles = "inline-flex items-center justify-center rounded-pill font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:pointer-events-none disabled:opacity-50 min-h-[48px]";
  
  const variants = {
    primary: "bg-primary text-white hover:bg-primary-hover active:bg-primary-active",
    secondary: "bg-secondary text-white hover:bg-secondary-hover",
    outline: "border-2 border-secondary text-secondary hover:bg-secondary-soft",
    alert: "bg-status-error text-white hover:bg-red-800",
    ghost: "text-secondary hover:bg-secondary-soft",
  };

  const sizes = {
    sm: "px-4 py-2 text-sm",
    md: "px-6 py-3 text-base min-h-[48px]",
    lg: "px-8 py-4 text-lg min-h-[56px]",
    icon: "h-12 w-12",
  };

  return (
    <button
      className={cn(baseStyles, variants[variant], sizes[size], className)}
      {...props}
    >
      {children}
    </button>
  );
}
