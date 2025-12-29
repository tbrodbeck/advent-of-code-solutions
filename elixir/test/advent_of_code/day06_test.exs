defmodule AdventOfCode.Day06Test do
  use ExUnit.Case

  alias AdventOfCode.Day06

  @example_input """
  123 328  51 64
   45 64  387 23
    6 98  215 314
  *   +   *   +
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day06.part1(@example_input) == 4_277_556
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day06.part2(@example_input) == 3_263_827
    end
  end
end
