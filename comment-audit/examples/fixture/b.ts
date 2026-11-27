/** Public API: returns the user id or null. */
export function id(u: User): string | null {
  // @ts-ignore
  const n = u.nmae; // TODO fix typo later
  const url = "http://x.com//path"; // trailing real comment
  /* multi
     line */
  return n ?? null;
}
