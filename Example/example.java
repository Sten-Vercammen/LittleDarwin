import java.util.ArrayList;
import java.lang.Runnable;




@FunctionalInterface
public interface Interface1 {

	void method1(String str);

	default void log(String str){
		System.out.println("I1 logging::"+str);

Runnable r1 = () -> {
			System.out.println("My Runnable");
		};

	}

	static void print(String str){
		System.out.println("Printing "+str);
	}
}



public class ExampleProgram {

    public static void exampleMethod(){
        int a = 1;
        int b = 2;

        String x = "Hello!";
        String y = "Hi!";
        ArrayList<String> array = new ArrayList<String>();

        String z;

        z = x + y;
        z = "Hi" + y;
        z =  'a' + y;
        z = 'a' == y;



        if (a==1) a += 1;

        else {
            if (b==2) b += 2;

            else a = 3;

        }

        a = 4;
        return;

   }

   public int exampleMethod2(int var1, String var2, ArrayList var3)
    {
        var1 = 25;

        var2 = "Hey!";

        if (var1 == null)
            {
            var2 = "Hoy!";
            }



        if (var3 != null)
            {
            var2 = "Hey";
            }

        return 1;
    }



   public ArrayList exampleMethod3(int var1, String var2, ArrayList var3)
    {
        var1 = 25;

        var2 = "Hey!";

        return var3;
    }


}