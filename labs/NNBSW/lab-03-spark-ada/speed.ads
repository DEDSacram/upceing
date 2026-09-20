--  SPARK package spec: speed supervision contracts.
package Speed with SPARK_Mode is

   subtype Speed_T is Natural range 0 .. 350;
   subtype Limit_T is Natural range 0 .. 350;

   function Is_Safe (S : Speed_T; L : Limit_T) return Boolean
     with Post => (Is_Safe'Result = (S <= L));

   procedure Clamp (S : in out Speed_T; L : in Limit_T)
     with Pre  => True,
          Post => (S <= L and S <= S'Old);

   function Brake_Distance (S : Speed_T) return Natural
     with Pre  => (S <= 350),
          Post => (Brake_Distance'Result >= S);

end Speed;
