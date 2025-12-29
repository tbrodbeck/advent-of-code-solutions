defmodule AdventOfCode.Day10Test do
  use ExUnit.Case

  alias AdventOfCode.Day10

  @example_input """
  [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day10.part1(@example_input) == 2
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day10.part2(@example_input) == 10
    end
  end
end
