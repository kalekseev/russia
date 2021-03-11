{ pkgs ? import <nixpkgs> { }, system ? builtins.currentSystem }:
with pkgs;
let
  src = fetchTarball {
    url = "https://github.com/numtide/devshell/archive/f64db97388dda7c2c6f8fb7aa5d6d08365fb1e01.tar.gz";
    sha256 = "1421h6bhsg4fishz10092m71qnd5ll6129l45kychzh9kp23040s";
  };
  devshell = import src { inherit system; };
  python = python3.withPackages (ps: [ ps.pandas ps.xlrd ps.ipython ]);
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
