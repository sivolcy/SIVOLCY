import { useLocation } from "react-router";
import { useTranslation } from "react-i18next";
import { I18nKey } from "#/i18n/declaration";
import { TooltipButton } from "./tooltip-button";
import PlusIcon from "#/icons/u-plus.svg?react";

interface NewProjectButtonProps {
  disabled?: boolean;
}

export function NewProjectButton({ disabled = false }: NewProjectButtonProps) {
  const { pathname } = useLocation();

  const { t } = useTranslation();

  const startNewProject = t(I18nKey.CONVERSATION$START_NEW);

  // 从 localStorage 获取 token
  const localToken =
    typeof window !== "undefined" ? localStorage.getItem("jwt_token") : null;

  // 根据是否存在 token 构建 navLinkTo 的路径
  // 如果 localToken 存在，则将它作为查询参数附带到根路径
  const pathToHome = localToken ? `/?token=${localToken}` : "/";

  return (
    <TooltipButton
      tooltip={startNewProject}
      ariaLabel={startNewProject}
      // navLinkTo="/"
      navLinkTo={pathToHome} // 使用动态构建的路径
      testId="new-project-button"
      disabled={disabled}
    >
      <PlusIcon
        width={24}
        height={24}
        color={pathname === "/" ? "#ffffff" : "#B1B9D3"}
      />
    </TooltipButton>
  );
}
