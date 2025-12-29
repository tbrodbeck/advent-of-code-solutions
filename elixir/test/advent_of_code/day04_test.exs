defmodule AdventOfCode.Day04Test do
  use ExUnit.Case

  alias AdventOfCode.Day04

  @example_input """
  @.@@
  @@.@
  .@@@
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day04.part1(@example_input) == 6
    end

    test "count_neighbors" do
      grid = Day04.parse_input(@example_input)
      assert Day04.count_neighbors(grid, 0, 0) == 2
      assert Day04.count_neighbors(grid, 1, 1) == 5
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day04.part2(@example_input) == 9
    end
  end
end
