{pkgs} : pkgs.python3Packages.buildPythonPackage rec {
  pname = "pymultinest";
  version = "2.11";
  nativeBuildInputs = [];
  propagatedBuildInputs = with pkgs.python3Packages; [numpy matplotlib scipy pytest-runner];
  buildInputs = [pkgs.multinest];
  doCheck = false;

  postUnpack = ''
substituteInPlace pymultinest-${version}/pymultinest/run.py \
 --replace "lib = _load_library('libmultinest')" "lib = cdll.LoadLibrary('${pkgs.multinest}/lib/libmultinest.so')" \
 --replace "lib_mpi = _load_library('libmultinest_mpi')" "lib_mpi = cdll.LoadLibrary('${pkgs.multinest}/lib/libmultinest_mpi.so')"
'';

  src = pkgs.python3Packages.fetchPypi {
    inherit pname version;
    hash = "sha256-uFPTdXh1QZgnof02HAVPM9sktzYMHvXbbckNLuUeB+w=";
  };
}
