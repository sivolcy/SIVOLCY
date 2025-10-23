import { useTranslation } from "react-i18next";
import { Typography } from "#/ui/typography";

export function HomeHeaderTitle() {
  const { t } = useTranslation();

  return (
    <div className="h-[80px] flex items-center">
      <Typography.H1 className="text-[#282828]">{t("HOME$LETS_START_BUILDING")}</Typography.H1>
    </div>
  );
}
