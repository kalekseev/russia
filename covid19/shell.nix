{ system ? builtins.currentSystem }:
let
  src = fetchTarball {
    url = "https://github.com/numtide/devshell/archive/f64db97388dda7c2c6f8fb7aa5d6d08365fb1e01.tar.gz";
    sha256 = "1421h6bhsg4fishz10092m71qnd5ll6129l45kychzh9kp23040s";
  };
  pkgsSrc = fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/3a2e0c36e79cecaf196cbea23e75e74710140ea4.tar.gz";
    sha256 = "0gjv2y6vjn3sdpg8ljcw2mk99c1xxdrfv11pc8kf5ms64wby20g5";
  };
  pkgs = import pkgsSrc { };
  devshell = import src { inherit system; };
  python = pkgs.python3.withPackages (ps: [ ps.pandas ps.xlrd ps.ipython ]);
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
