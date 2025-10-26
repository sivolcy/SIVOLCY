import { useTranslation } from "react-i18next";
import posthog from "posthog-js";
import PRIcon from "#/icons/u-pr.svg?react";
import { cn, getCreatePRPrompt } from "#/utils/utils";
import { useUserProviders } from "#/hooks/use-user-providers";
import { I18nKey } from "#/i18n/declaration";
import { Provider } from "#/types/settings";

interface GitControlBarPrButtonProps {
  onSuggestionsClick: (value: string) => void;
  hasRepository: boolean;
  currentGitProvider: Provider;
}

export function GitControlBarPrButton({
  onSuggestionsClick,
  hasRepository,
  currentGitProvider,
}: GitControlBarPrButtonProps) {
  const { t } = useTranslation();

  const { providers } = useUserProviders();

  const providersAreSet = providers.length > 0;
  const isButtonEnabled = providersAreSet && hasRepository;

  const handlePrClick = () => {
    posthog.capture("create_pr_button_clicked");
    onSuggestionsClick(getCreatePRPrompt(currentGitProvider));
  };

  return (
    <button
      type="button"
      onClick={handlePrClick}
      disabled={!isButtonEnabled}
      className={cn(
        "flex flex-row gap-1 items-center justify-center px-2 py-1 rounded-[100px] w-[126px] min-w-[126px] h-7",
        "bg-white hover:bg-gray-100 border border-gray-300",
        isButtonEnabled ? "cursor-pointer" : "cursor-not-allowed",
      )}
    >
      <div className="w-3 h-3 flex items-center justify-center">
        <PRIcon width={12} height={12} color="black" />
      </div>
      <div
        className="font-normal text-sm leading-5 max-w-[126px] truncate text-black"
        title={t(I18nKey.COMMON$PULL_REQUEST)}
      >
        {t(I18nKey.COMMON$PULL_REQUEST)}
      </div>
    </button>
  );
}
