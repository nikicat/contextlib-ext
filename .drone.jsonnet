local Pipeline(toxenv, image) = {
  kind: "pipeline",
  name: toxenv,
  steps: [
    {
      name: "test",
      image: image,
      commands: [
        "pip install tox",
        "tox -e " + toxenv
      ]
    }
  ]
};

[
  Pipeline("py37", "python:3.7"),
  Pipeline("py38", "python:3.8"),
]
