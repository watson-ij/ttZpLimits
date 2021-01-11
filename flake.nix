{
  description = "A very basic flake";

  outputs = { self, nixpkgs }: {

    overlay = final: prev: { # pymultinest = prev.callPackage ./nix/pymultinest.nix {};
      multinest = prev.callPackage ./nix/multinest.nix {};
      mypython = final.python3.override {
        packageOverrides = psuper: pprev: { pymultinest = psuper.callPackage ./nix/pymultinest.nix {}; };
      };
    };

    packages.x86_64-linux.hello = nixpkgs.legacyPackages.x86_64-linux.hello;

    # defaultPackage.x86_64-linux = with import nixpkgs {system="x86_64-linux"; overlays=[self.overlay];}; buildEnv {
    #   buil
    # };

    devShell.x86_64-linux = with import nixpkgs {system="x86_64-linux"; overlays=[self.overlay];}; mkShell {
      buildInputs = [(mypython.withPackages (ps: with ps; [pymultinest mpi4py numpy scipy matplotlib]))];
    };
    defaultShell.x86_64-linux = with import nixpkgs {system="x86_64-linux"; overlays=[self.overlay];}; mkShell {
      builtInputs = [mypython];
    };

  };
}
