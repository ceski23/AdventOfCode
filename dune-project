(lang dune 3.11)

(generate_opam_files true)

(map_workspace_root false)

(package
 (name aoc)
 (authors "Cezary Bober")
 (maintainers "Cezary Bober")
 (homepage "https://github.com/ceski23/AdventOfCode")
 (bug_reports "https://github.com/ceski23/AdventOfCode/issues")
 (synopsis "Advent of Code task done in OCaml")
 (depends
  (ocaml
   (>= 4.08.0))
  (re2
   (>= 0.16.0))
  (core
   (>= 0.16.0))))
