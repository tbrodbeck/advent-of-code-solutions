defmodule AdventOfCode.Day01Test do
  use ExUnit.Case

  alias AdventOfCode.Day01

  @example_input """
  L68
  L30
  R48
  L5
  R60
  L55
  L1
  L99
  R14
  L82
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day01.part1(@example_input) == 3
    end

    test "land on zero" do
      assert Day01.part1("R50") == 1
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day01.part2(@example_input) == 6
    end

    test "right to zero" do
      assert Day01.part2("R50") == 1
    end

    test "left cross" do
      assert Day01.part2("L55") == 1
    end

    test "left land" do
      assert Day01.part2("L50") == 1
    end

    test "right multi wrap" do
      assert Day01.part2("R150") == 2
    end

    test "no cross" do
      assert Day01.part2("R10") == 0
    end

    test "left from zero" do
      assert Day01.part2("R50\nL5") == 1
    end

    test "left full circle" do
      assert Day01.part2("R50\nL100") == 2
    end
  end
end
