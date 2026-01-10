{pkgs, ...}: {
  languages = {
    python = {
      enable = true;
      uv = {
        enable = true;
        sync.enable = true;
      };
    };
  };

  treefmt = {
    enable = true;
    config.programs = {
      actionlint.enable = true;
      # Nix
      alejandra.enable = true;
      statix.enable = true;
      # Rust
      rustfmt.enable = true;
      # Python
      ruff-check.enable = true;
      ruff-format.enable = true;
      # Shell
      shfmt.enable = true;
      shellcheck.enable = true;
      # Markdown
      mdformat.enable = true;
      # TOML
      taplo.enable = true;
      # YAML
      yamlfmt.enable = true;
      # JSON
      formatjson5.enable = true;
      # Just
      just.enable = true;
      # Spelling
      typos.enable = true;
      autocorrect.enable = true;
    };
  };

  git-hooks.package = pkgs.prek;
  git-hooks.hooks = {
    # Format
    treefmt.enable = true;
    # Python
    uv-lock.enable = true;
    # Git
    check-branch = {
      enable = true;
      name = "Check branch name";
      entry = "uvx commit-check --branch";
      language = "system";
      pass_filenames = false;
    };
  };
  # See full reference at https://devenv.sh/reference/options/
}
