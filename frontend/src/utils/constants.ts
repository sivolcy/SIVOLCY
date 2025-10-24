export const ASSET_FILE_TYPES = [
  ".png",
  ".jpg",
  ".jpeg",
  ".bmp",
  ".gif",
  ".pdf",
  ".mp4",
  ".webm",
  ".ogg",
];

export const JSON_VIEW_THEME = {
  base00: "transparent", // background
  base01: "#f8f9fa", // lighter background
  base02: "#e9ecef", // selection background
  base03: "#6c757d", // comments, invisibles
  base04: "#495057", // dark foreground
  base05: "#212529", // default foreground
  base06: "#343a40", // light foreground
  base07: "#ffffff", // light background
  base08: "#dc3545", // variables, red
  base09: "#fd7e14", // integers, orange
  base0A: "#ffc107", // booleans, yellow
  base0B: "#28a745", // strings, green
  base0C: "#17a2b8", // support, cyan
  base0D: "#007bff", // functions, blue
  base0E: "#6f42c1", // keywords, purple
  base0F: "#dc3545", // deprecated, red
};

export const DOCUMENTATION_URL = {
  MICROAGENTS: {
    MICROAGENTS_OVERVIEW:
      "https://docs.all-hands.dev/usage/prompting/microagents-overview",
    ORGANIZATION_AND_USER_MICROAGENTS:
      "https://docs.all-hands.dev/usage/prompting/microagents-org",
  },
};

export const PRODUCT_URL = {
  PRODUCTION: "https://app.all-hands.dev",
};

export const SETTINGS_FORM = {
  LABEL_CLASSNAME:
    "text-[11px] font-medium leading-4 tracking-[0.11px] text-white",
};

export const GIT_PROVIDER_OPTIONS = [
  {
    label: "GitHub",
    value: "github",
  },
  {
    label: "GitLab",
    value: "gitlab",
  },
  {
    label: "Bitbucket",
    value: "bitbucket",
  },
];

export const CONTEXT_MENU_ICON_TEXT_CLASSNAME = "h-[30px]";

// Chat input constants
export const CHAT_INPUT = {
  HEIGHT_THRESHOLD: 100, // Height in pixels when suggestions should be hidden
};

// UI tolerance constants
export const EPS = 1.5; // px tolerance for "near min" height comparisons
