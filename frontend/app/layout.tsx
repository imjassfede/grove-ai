import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Growth AI — Turn business problems into strategic intelligence",
  description:
    "AI-powered growth intelligence platform that transforms business challenges into root cause analysis, strategic insights, and actionable recommendations.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
