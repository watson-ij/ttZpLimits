{pkgs} :
with pkgs; gcc6Stdenv.mkDerivation rec {
  pname = "multinest";
  version = "3.10b";
  src = fetchurl {
    url = "https://github.com/JohannesBuchner/MultiNest/archive/v3.10b.tar.gz";
    hash = "sha256-PuNBoGPviby7259CRPFGm8cYgUrzC+qhWCYX96Nt6to=";
  };
  nativeBuildInputs = [cmake gfortran];
  buildInputs = [openblas openmpi];
  configurePhase = "cd build
cmake -DCMAKE_INSTALL_PREFIX=$out/ ..
make # need to build in order
make install
";
  buildPhase = ''echo done'';
  installPhase = ''echo done'';
}
