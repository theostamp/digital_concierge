export function Button({ children, className = "", variant = "default" }: any) {
  const style =
    variant === "outline"
      ? "border border-gray-300 text-gray-700 bg-white hover:bg-gray-50"
      : "bg-blue-600 text-white hover:bg-blue-700";

  return <button className={`rounded px-4 py-2 ${style} ${className}`}>{children}</button>;
}
