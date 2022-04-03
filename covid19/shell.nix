{ system ? builtins.currentSystem }:
let
  pkgsSrc = fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/bacc31ff571ece62147f3ba70cb6d8d8f483a949.tar.gz";
    sha256 = "1wbgry1as0867bk5mmx3954pya41j34b3g6af4dpah9mh1ai2jc6";
  };
  devshellSrc = fetchTarball {
    url = "https://github.com/numtide/devshell/archive/f87fb932740abe1c1b46f6edd8a36ade17881666.tar.gz";
    sha256 = "10cimkql88h7jfjli89i8my8j5la91zm4c78djqlk22dqrxmm6bs";
  };
  pkgs = import pkgsSrc { };
  devshell = import devshellSrc { inherit system; };
  python = pkgs.python3.withPackages (ps: [ ps.pandas ps.xlrd ps.ipython ps.openpyxl ]);
in
devshell.mkShell {
  name = "russia";
  packages = [
    python
  ];
  commands = [
    {
      help = "pull stopcoronavirus data";
      name = "pull.stopcoronavirus";
      command = "make pull.stopcoronavirus";
    }
    {
      help = "start http server";
      name = "start";
      command = "make start";
    }
  ];
}
