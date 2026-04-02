import React from "react";
import { cn } from "../../lib/utils";

export function Card({ className, children, ...props }) {
  return (
    <div
      className={cn(
        "rounded-md border border-secondary-soft bg-background-surface text-text-primary shadow-sm",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className, children, ...props }) {
  return (
    <div className={cn("flex flex-col space-y-1.5 p-6", className)} {...props}>
      {children}
    </div>
  );
}

export function CardContent({ className, children, ...props }) {
  return (
    <div className={cn("p-6 pt-0", className)} {...props}>
      {children}
    </div>
  );
}
