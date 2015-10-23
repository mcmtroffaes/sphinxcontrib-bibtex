# Script for setting up a quick development shell for running tox.
#
# Usage:
#
#     nix-shell --run tox

with import <nixpkgs> {}; {
  my-env = stdenv.mkDerivation {
    name = "my-env";
    buildInputs = [
      # python versions that we test
      python27
      python33
      python34
      # development tools and libraries
      stdenv
      libxml2
      libxslt
      python27Packages.tox
      python27Packages.cython
    ];
  };
}
