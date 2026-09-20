--  SPARK package body with a loop invariant example.
package body Speed with SPARK_Mode is

   function Is_Safe (S : Speed_T; L : Limit_T) return Boolean is
   begin
      return S <= L;
   end Is_Safe;

   procedure Clamp (S : in out Speed_T; L : in Limit_T) is
   begin
      if S > L then
         S := L;
      end if;
   end Clamp;

   function Brake_Distance (S : Speed_T) return Natural is
      D : Natural := 0;
      V : Natural := S;
   begin
      while V > 0 loop
         pragma Loop_Invariant (D + V >= S and V <= S);
         pragma Loop_Variant (Decreases => V);
         D := D + 1;
         V := V - 1;
      end loop;
      pragma Assert (D >= S);
      return D;
   end Brake_Distance;

end Speed;
