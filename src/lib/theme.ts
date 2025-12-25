/**
 * Shared theme configuration
 * Centralized color definitions for consistent UI across components
 */

export interface ThemeColors {
  // Base colors
  bg: string;
  cardBg: string;
  border: string;
  text: string;
  textMuted: string;

  // Node colors
  inputColor: string;
  encodingColor: string;
  outputColor: string;

  // Canvas colors
  dotColor: string;
  maskColor: string;

  // UI colors
  primary: string;
  primaryText: string;
  secondary: string;
  mutedColor: string;

  // Button colors
  buttonBg: string;
  buttonText: string;
}

export const themes: Record<'dark' | 'light', ThemeColors> = {
  dark: {
    // Base
    bg: '#0f172a',
    cardBg: '#1e293b',
    border: '#334155',
    text: '#f1f5f9',
    textMuted: '#94a3b8',

    // Nodes
    inputColor: '#3b82f6',
    encodingColor: '#10b981',
    outputColor: '#eab308',

    // Canvas
    dotColor: 'rgba(148, 163, 184, 0.3)',
    maskColor: 'rgba(15, 23, 42, 0.8)',

    // UI
    primary: '#3b82f6',
    primaryText: '#ffffff',
    secondary: '#1e293b',
    mutedColor: '#64748b',

    // Buttons
    buttonBg: '#1e293b',
    buttonText: '#f1f5f9',
  },
  light: {
    // Base
    bg: '#f8fafc',
    cardBg: '#ffffff',
    border: '#e2e8f0',
    text: '#1e293b',
    textMuted: '#64748b',

    // Nodes
    inputColor: '#2563eb',
    encodingColor: '#059669',
    outputColor: '#ca8a04',

    // Canvas
    dotColor: 'rgba(100, 116, 139, 0.3)',
    maskColor: 'rgba(248, 250, 252, 0.8)',

    // UI
    primary: '#3b82f6',
    primaryText: '#ffffff',
    secondary: '#f1f5f9',
    mutedColor: '#94a3b8',

    // Buttons
    buttonBg: '#f1f5f9',
    buttonText: '#1e293b',
  },
};

/**
 * Get theme colors based on theme mode
 */
export function getTheme(mode: 'dark' | 'light'): ThemeColors {
  return themes[mode];
}
