import { clsx } from "clsx";

const variants = {
  red: "bg-red-500/20 text-red-300 border-red-500/30",
  orange: "bg-orange-500/20 text-orange-300 border-orange-500/30",
  purple: "bg-purple-500/20 text-purple-300 border-purple-500/30",
  green: "bg-green-500/20 text-green-300 border-green-500/30",
  amber: "bg-amber-500/20 text-amber-300 border-amber-500/30",
  blue: "bg-blue-500/20 text-blue-300 border-blue-500/30",
  gray: "bg-white/10 text-white/60 border-white/20",
};

interface BadgeProps {
  label: string;
  variant?: keyof typeof variants;
  className?: string;
}

export function Badge({ label, variant = "gray", className }: BadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold uppercase tracking-wider border",
        variants[variant],
        className
      )}
    >
      {label}
    </span>
  );
}
