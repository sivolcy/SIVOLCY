interface ServerStatusContextMenuIconTextProps {
  icon: React.ReactNode;
  text: string;
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
  testId?: string;
}

export function ServerStatusContextMenuIconText({
  icon,
  text,
  onClick,
  testId,
}: ServerStatusContextMenuIconTextProps) {
  return (
    <button
      className="flex items-center gap-2 p-2 hover:bg-[var(--attachment-bg)] rounded text-sm text-white font-normal leading-5 cursor-pointer w-full"
      onClick={onClick}
      data-testid={testId}
      type="button"
    >
      {text}
      {icon}
    </button>
  );
}
