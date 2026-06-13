"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";

/**
 * Hover-to-open primary navigation.
 *
 * Behavior:
 *   - Mouse:    hover trigger to open; cursor can cross 16px bridge into the panel;
 *               close ~140ms after pointerleave so the cursor doesn't lose the menu.
 *   - Touch:    hover suppressed; tap toggles.
 *   - Keyboard: focus opens; tab cycles items; Escape closes; outside click closes.
 *
 * Pair with assets/hover-nav.css.
 */

const HOVER_CLOSE_DELAY_MS = 140;

type NavItem = { href: string; label: string; description?: string };
type NavGroup = { label: string; items: NavItem[] };

interface HoverNavProps {
  groups: NavGroup[];
  /** Extra single links rendered after the dropdown groups (e.g. "Case studies", "How we work"). */
  extraLinks?: NavItem[];
  /** Optional primary CTA at the end of the nav. */
  cta?: { href: string; label: string };
  /** Mobile drawer open state controlled by parent (so a hamburger button can live elsewhere in the header). */
  drawerOpen?: boolean;
}

export function HoverNav({ groups, extraLinks = [], cta, drawerOpen = false }: HoverNavProps) {
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const navRef = useRef<HTMLElement | null>(null);
  const pathname = usePathname();

  const clearCloseTimer = useCallback(() => {
    if (closeTimer.current) {
      clearTimeout(closeTimer.current);
      closeTimer.current = null;
    }
  }, []);

  const scheduleClose = useCallback(() => {
    clearCloseTimer();
    closeTimer.current = setTimeout(() => setOpenMenu(null), HOVER_CLOSE_DELAY_MS);
  }, [clearCloseTimer]);

  const openNow = useCallback(
    (label: string) => {
      clearCloseTimer();
      setOpenMenu(label);
    },
    [clearCloseTimer]
  );

  useEffect(() => setOpenMenu(null), [pathname]);

  useEffect(() => {
    const onPointerDown = (event: PointerEvent) => {
      if (navRef.current && !navRef.current.contains(event.target as Node)) {
        setOpenMenu(null);
      }
    };
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpenMenu(null);
    };
    document.addEventListener("pointerdown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
      clearCloseTimer();
    };
  }, [clearCloseTimer]);

  const isActive = (href: string) => pathname === href || pathname.startsWith(`${href}/`);

  return (
    <nav
      ref={navRef}
      className={`primary-nav${drawerOpen ? " is-open" : ""}`}
      aria-label="Primary navigation"
    >
      {groups.map((group) => {
        const isOpen = openMenu === group.label;
        return (
          <div
            key={group.label}
            className="nav-menu"
            data-open={isOpen ? "true" : "false"}
            onPointerEnter={(e) => {
              if (e.pointerType === "touch") return;
              openNow(group.label);
            }}
            onPointerLeave={(e) => {
              if (e.pointerType === "touch") return;
              scheduleClose();
            }}
            onFocus={() => openNow(group.label)}
            onBlur={(e) => {
              if (!e.currentTarget.contains(e.relatedTarget as Node)) scheduleClose();
            }}
          >
            <button
              type="button"
              className="nav-summary"
              aria-expanded={isOpen}
              aria-haspopup="true"
              onClick={() => setOpenMenu(isOpen ? null : group.label)}
            >
              {group.label}
            </button>
            <div className="nav-panel" role="menu" aria-hidden={!isOpen}>
              {group.items.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  role="menuitem"
                  tabIndex={isOpen ? 0 : -1}
                  className={isActive(item.href) ? "is-active" : undefined}
                  aria-current={isActive(item.href) ? "page" : undefined}
                >
                  {item.label}
                  {item.description && <span>{item.description}</span>}
                </Link>
              ))}
            </div>
          </div>
        );
      })}

      {extraLinks.map((link) => (
        <Link
          key={link.href}
          href={link.href}
          className={isActive(link.href) ? "is-active" : undefined}
          aria-current={isActive(link.href) ? "page" : undefined}
        >
          {link.label}
        </Link>
      ))}

      {cta && (
        <Link href={cta.href} className="button button-accent nav-cta">
          {cta.label}
        </Link>
      )}
    </nav>
  );
}
