defmodule AdventOfCode.Day12Test do
  use ExUnit.Case

  alias AdventOfCode.Day12

  @example_input """
  0:
  ###
  ##.
  ##.

  1:
  ###
  ##.
  .##

  2:
  .##
  ###
  ##.

  3:
  ##.
  ###
  ##.

  4:
  ###
  #..
  ###

  5:
  ###
  .#.
  ###

  4x4: 0 0 0 0 2 0
  12x5: 1 0 1 0 2 2
  12x5: 1 0 1 0 3 2
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day12.part1(@example_input) == 2
    end
  end
end
