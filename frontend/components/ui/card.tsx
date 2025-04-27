// components/ui/card.tsx

import { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
}

export function UICard({ children, className }: CardProps) {
  return <div className={`rounded-xl border bg-white ${className}`}>{children}</div>;
}

export function UICardContent({ children, className }: CardProps) {
  return <div className={`p-4 ${className}`}>{children}</div>;
}