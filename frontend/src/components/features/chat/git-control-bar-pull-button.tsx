import { useTranslation } from "react-i18next";
import posthog from "posthog-js";
import ArrowDownIcon from "#/icons/u-arrow-down.svg?react";
import { cn, getGitPullPrompt } from "#/utils/utils";
import { useActiveConversation } from "#/hooks/query/use-active-conversation";
import { useUserProviders } from "#/hooks/use-user-providers";
import { I18nKey } from "#/i18n/declaration";

interface GitControlBarPullButtonProps {
  onSuggestionsClick: (value: string) => void;
}

export function GitControlBarPullButton({
  onSuggestionsClick,
}: GitControlBarPullButtonProps) {
  const { t } = useTranslation();

  const { data: conversation } = useActiveConversation();
  const { providers } = useUserProviders();

  const providersAreSet = providers.length > 0;
  const hasRepository = conversation?.selected_repository;
  const isButtonEnabled = providersAreSet && hasRepository;

  const handlePullClick = () => {
    posthog.capture("pull_button_clicked");
    onSuggestionsClick(getGitPullPrompt());
  };

  return (
    <button
      type="button"
      onClick={handlePullClick}
      disabled={!isButtonEnabled}
      className={cn(
        "flex flex-row gap-1 items-center justify-center px-0.5 py-1 rounded-[100px] w-[76px] min-w-[76px]",
        "bg-white hover:bg-gray-100 border border-gray-300",
        isButtonEnabled ? "cursor-pointer" : "cursor-not-allowed",
      )}
    >
      <div className="w-3 h-3 flex items-center justify-center">
        <ArrowDownIcon width={12} height={12} color="black" />
      </div>
      <div
        className="font-normal text-sm leading-5 max-w-[76px] truncate text-black"
        title={t(I18nKey.COMMON$PULL)}
      >
        {t(I18nKey.COMMON$PULL)}
      </div>
    </button>
  );
}
