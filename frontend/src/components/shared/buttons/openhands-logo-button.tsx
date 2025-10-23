import CompareGPTLogo from "#/assets/branding/comparegpt-logo.svg?react";
import { TooltipButton } from "./tooltip-button";

export function OpenHandsLogoButton() {
  return (
    <TooltipButton
      tooltip="CompareGPT"
      ariaLabel="CompareGPT Logo"
      navLinkTo="/"
    >
      <CompareGPTLogo width={46} height={30} />
    </TooltipButton>
  );
}
