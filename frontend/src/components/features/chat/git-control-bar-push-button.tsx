import { useTranslation } from "react-i18next";
import posthog from "posthog-js";
import ArrowUpIcon from "#/icons/u-arrow-up.svg?react";
import { cn, getGitPushPrompt } from "#/utils/utils";
import { useUserProviders } from "#/hooks/use-user-providers";
import { I18nKey } from "#/i18n/declaration";
import { Provider } from "#/types/settings";

interface GitControlBarPushButtonProps {
  onSuggestionsClick: (value: string) => void;
  hasRepository: boolean;
  currentGitProvider: Provider;
}

export function GitControlBarPushButton({
  onSuggestionsClick,
  hasRepository,
  currentGitProvider,
}: GitControlBarPushButtonProps) {
  const { t } = useTranslation();

  const { providers } = useUserProviders();

  const providersAreSet = providers.length > 0;
  const isButtonEnabled = providersAreSet && hasRepository;

  const handlePushClick = () => {
    posthog.capture("push_button_clicked");
    onSuggestionsClick(getGitPushPrompt(currentGitProvider));
  };

  return (
    <button
      type="button"
      onClick={handlePushClick}
      disabled={!isButtonEnabled}
      className={cn(
        "flex flex-row gap-1 items-center justify-center px-2 py-1 rounded-[100px] w-[77px] min-w-[77px]",
        isButtonEnabled
          ? "bg-white hover:bg-gray-100 cursor-pointer border border-gray-300"
          : "bg-[rgba(71,74,84,0.50)] cursor-not-allowed",
      )}
    >
      <div className="w-3 h-3 flex items-center justify-center">
        <ArrowUpIcon width={12} height={12} color={isButtonEnabled ? "black" : "white"} />
      </div>
      <div
        className={cn(
          "font-normal text-sm leading-5 max-w-[77px] truncate",
          isButtonEnabled ? "text-black" : "text-white"
        )}
        title={t(I18nKey.COMMON$PUSH)}
      >
        {t(I18nKey.COMMON$PUSH)}
      </div>
    </button>
  );
}
