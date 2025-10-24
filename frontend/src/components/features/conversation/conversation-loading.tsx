import { LoaderCircle } from "lucide-react";
import { useTranslation } from "react-i18next";
import { I18nKey } from "#/i18n/declaration";

export function ConversationLoading() {
  const { t } = useTranslation();

  return (
    <div className="bg-[#EAEAEA] border border-gray-400 rounded-xl flex flex-col items-center justify-center h-full w-full">
      <LoaderCircle className="animate-spin w-16 h-16" color="black" />
      <span className="text-2xl font-normal leading-5 text-black p-4">
        {t(I18nKey.HOME$LOADING)}
      </span>
    </div>
  );
}
