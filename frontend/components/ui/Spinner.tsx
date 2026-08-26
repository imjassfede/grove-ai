import { clsx } from "clsx";

export function Spinner({ className }: { className?: string }) {
  return (
    <div
      className={clsx(
        "w-5 h-5 rounded-full border-2 border-white/20 border-t-blue-500 animate-spin",
        className
      )}
    />
  );
}
