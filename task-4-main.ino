/*
  Team Id:          e-YRC#5352
  Author list:      Gade Atul, Mujahid Atar, Sujata Patil
  File name:        task-4-main.ino
  Theme name:       Ant Bot
  Functions:        Back(), Read(), Frd(), Left(), Right(), Stop(), SharpLeft(), SharpRight(), Scan_Aruco(), SlowRight(), SlowLeft(), Line_Follow(),Scan_Supply(), check()
                    full_pick(), full_place(), half_pick(), half_place(), Get_Supply(), AH_Services(), Pick_AH0(), Pick_AH1(), Pick_AH2(), Pick_AH3(), Check_Array1(), Check_Array2(),
                    Pick_Serv1(), Pick_Serv2(), Goto_node0(), Goto_node1(), Goto_node2(), Goto_node3(), Goto_node4(), Goto_node5(), Comeback0(), Comeback1(), Comeback2(),
                    Comeback3(), Comeback4(), Comeback5(), Goto_AH0(), Goto_AH1(), Goto_AH2(), Goto_AH3(), ComeTO_Start0(), ComeTO_Start1(),ComeTO_Start2(), ComeTO_Start3(),
                    Trash_Deposit0(), Trash_Deposit1(), Trash_Deposit2(), Trash_Deposit3(), Place_Service()
  Global variables: LS, MS, RS, RE, LE, RF, LF, RB, LB, n, i, r, j, b, node, Buzz, rec, Array[], AH, Serv2, Serv1, TR,
*/
#include<Servo.h>                                                                                // Library file for servo motor
Servo servo_motor;                                                                               // vertical axial movement motor
Servo std_motor;                                                                                 // horizontal axial movement motor

/// ****  Declaration of varibles used in programm *** ////
int LS, MS, RS;                                                                                  // Variables for middle sensor
int RE = 4;                                                                                      // Right Motor Enable
int LE = 9;                                                                                      // Left Motor Enable
int RF = 7;                                                                                      // Right Motor Forward
int RB = 8;                                                                                      // Right Motor Backward
int LF = 5;                                                                                      // Left Motor Forward
int LB = 6;                                                                                      // Left Motor Backward
int Buzz = 12;                                                                                   // Buzzer
int n, i, r, j, b, node = 0;
char rec ;                                                                                       // Varible to store received char
char Array[] = {};                                                                               // Array to store scanned supply 
char AH;                                                                                         // Store AH sequence
char Serv2;                                                                                      // Store service 2 of AH
char Serv1;                                                                                      // Store service 1 of AH
char TR;                                                                                         // Store trash removal of AH
void Back(void);


/// ****  Declaration of functions used in programm *** ////
void Read(void);
void Frd(void);
void Left(void);
void Right(void);
void Stop(void);
void SharpLeft(void);
void SharpRight(void);
void Scan_Aruco(void);
void SlowRight(void);
void SlowLeft(void);
void Line_Follow(void);
void Scan_Supply(void);
void check(void);
void full_pick(void);
void full_place(void);
void half_pick(void);
void half_place(void);
void Get_Supply(void);
void AH_Services(void);
void Pick_AH0(void);
void Pick_AH1(void);
void Pick_AH2(void);
void Pick_Ah3(void);
void Check_Array1(void);
void Check_Array2(void);
void Pick_Serv1(void);
void Pick_Serv2(void);
void Goto_node0(void);
void Goto_node1(void);
void Goto_node2(void);
void Goto_node3(void);
void Goto_node4(void);
void Goto_node5(void);
void Comeback0(void);
void Comeback1(void);
void Comeback2(void);
void Comeback3(void);
void Comeback4(void);
void Comeback5(void);
void Goto_AH0(void);
void Goto_AH1(void);
void Goto_AH2(void);
void Goto_AH3(void);
void ComeTO_Start0(void);
void ComeTO_Start1(void);
void ComeTO_Start2(void);
void ComeTO_Start3(void);
void Trash_Deposit0(void);
void Trash_Deposit1(void);
void Trash_Deposit2(void);
void Trash_Deposit3(void);
void Place_Service(void);


unsigned long THRESHOLD = 50;                                                                     // Line Sensor Avarage Value



/// *** Setup the required pin as output or input ***///
void setup()
{
  Serial.begin(9600);                                                                            // Baud rate for serial communication
  pinMode(A0, INPUT);                                                                            // Declare pin nas input for line sensor
  pinMode(A1, INPUT);                                                                            // Declare pin nas input for line sensor
  pinMode(A2, INPUT);                                                                            // Declare pin nas input for line sensor
  pinMode(RF, OUTPUT);                                                                        
  pinMode(RB, OUTPUT);
  pinMode(LF, OUTPUT);
  pinMode(LB, OUTPUT);
  pinMode(RE, OUTPUT);
  pinMode(LE, OUTPUT);
  pinMode(Buzz, OUTPUT);
  servo_motor.attach(2);                                                                         // Attach servo motor 
  std_motor.attach(3);                                                                           // Attach servo motor
  servo_motor.write(0);                                                                          // Set servo motor to 0 position
  std_motor.write(0);                                                                            // Set servo motor to 0 position

}


/// **** Main program start here ** DO NOT EDIT !!!! ///
void loop()
{
  if (Serial.available() > 0)                                                                   // Check received Data From RPi
  {
    rec = Serial.read();                                                                        // Stored received data
  }
  if (rec == 'S')                                                                               // Check for scannning of supply block
  {
    rec = 0;
    while (n <= 13)
    {
      Scan_Supply();                                                                            // Scan shrub area for supply
    }
    n = 0;
    Stop();                                                                                     // Stop ant bot 
    delay(200);
    Get_Supply();                                                                               // Gives supply block array
    n = 0;                                                                                      // Variable to count node
    while (n <= 1)                                                                              // count the node
    {
      Scan_Aruco();                                                                             // Scan ArUco 
    }
    n = 0;
    AH_Services();                                                                              // get service for AH
  }

}


//// **** Line follow is used to follow black line **** ////

void Line_Follow(void)
{
  Read();                                                                                     // Read analog sensor values
  if (LS <= THRESHOLD && MS >= THRESHOLD && RS <= THRESHOLD)                                  // if only middle sensor is high
  {
    Frd();                                                                                    // Move Forward

  }

  else if (LS < THRESHOLD && MS < THRESHOLD && RS < THRESHOLD)                                //if all sensor are low
  {
    Frd();                                                                                    // Move backward
  }

  else if (LS <= THRESHOLD && MS <= THRESHOLD && RS >= THRESHOLD)                             //if right sensor is high
  {
    Right();                                                                                  // Turn right

  }

  else if (LS >= THRESHOLD && MS <= THRESHOLD && RS <= THRESHOLD)                            //if left sensor is high
  {
    Left();                                                                                  // turn left

  }

  else if ((LS >= 100 && MS >= 100) || (MS >= 100 && RS >= 100))                             // if all sensors are high
  {
    Frd();
    while ((LS >= 100 && MS >= 100) || (MS >= 100 && RS >= 100))
    {
      Read();
    }
    n++;                                                                                    // Increament node 

  }

}


/// **** function used to scan shrub area for supply detection ****///
void Scan_Supply(void)
{
  Line_Follow();
  if (n != r)                                                                             // check the new and pre counted node if different then proceed
  {
    r = n;                                                                                // mark node as scanned                                                                          
    switch (n)
    {
      case 1:
        Frd();
        break;
      case 2:
        Frd();
        delay(100);
        SlowRight();
        delay(400);
        MS = 0;
        while (MS < 100)                                                                // Turn right untill line is detected
        {
          Read();
        }
        break;


      case 5:
        {
          Frd();
          j = 1;                                                                       
          delay(100);
          SlowLeft();
          MS = 0;
          while (MS < 50)                                                                     // Turn left untill black line is detected
          {
            Read();
          }
          Stop();
          check();                                                                            // Check the color of supply block
          delay(3000);
          i++;                                                                                // Increament node
          delay(200);
        }
        break;

      case 6:
        {
          Stop();
          check();
          delay(3000);
          i++;
          delay(200);
          //Frd();
        }
        break;

      case 7:
        {
          Stop();

          check();
          delay(3000);
          i++;
          delay(200);
          //Frd();
        }
        break;

      case 9:
        {
          Stop();
          check();
          delay(3000);
          i++;
          delay(200);
          //Frd();
        }
        break;
      case 8:
        {
          Frd();

        }
        break;

      case 10:
        {
          Stop();
          check();
          delay(3000);
          i++;
          delay(200);
          //Frd();
        }
        break;

      case 11:
        {
          Stop();
          delay(200);
          check();
          delay(3000);
          i++;
          Frd();
          delay(130);
          SlowRight();
          MS = 0;
          while (MS < 75)
          {
            Read();
          }
          delay(100);
        }
        break;

      case 14:
        Frd();
        delay(100);
        SlowLeft();
        delay(100);
        LS = 0;
        while (LS < 50)
        {
          Read();
        }
        Stop();
        delay(1000);
        break;
    }
  }
}

//// **** Store scanned supply block in array **** ////
void Get_Supply(void)
{
  Serial.println("S");
  while (n <= 5)
  {
    while (Serial.available() == 0);
    if (Serial.available() > 0)
    {
      rec = Serial.read();
      Array[n] = rec;
      n++;
    }
  }
}




//// **** functions to scan the Aruco **** ////
void Scan_Aruco(void)                  
{
  Line_Follow();                                                                                // Follow the line
  if (n != r)
  {
    r = n;
    Serial.println(n);
    switch (n)
    {

      case 1 :
        SharpLeft();
        delay(400);
        Stop();
        delay(1000);
        SharpRight();
        delay(580);
        Stop();
        delay(1000);
        SharpRight();
        delay(510);
        Stop();
        delay(1000);
        SharpRight();
        delay(650);
        Stop();
        delay(1000);
        SlowLeft();
        LS = 0;
        while (LS < 50)
        {
          Read();
        }
        Stop();
        break;
      case 2:
        Stop();
        delay(1000);

    }

  }
}

//// **** check function is used to check the color of supply block received from pi **** ////
void check(void)
{
  if (i != j)                                                                                   // Check that same color is not received
  {
    j = i;                                                                                      // Mark latest color as received color
    Serial.println("C");
    //while(Serial.available()==0);
    if (Serial.available() > 0)                                                                 // Receive Data From RPi
    {
      rec = Serial.read();
    }
    return ;
  }

}

//// **** this function used to check the services required for AH **** ////
void AH_Services()
{
  while (j <= 3)
  {
    Serial.print('P');                                                          // Receive AH no as character  from pi
    while (Serial.available() == 0);
    if (Serial.available() > 0)
    {
      rec = Serial.read();
      AH = rec;                                                                                                            
    }
    Serial.println('Q');                                                       // Receive serv2 for AH in the form of character from pi
    while (Serial.available() == 0);
    if (Serial.available() > 0)
    {
      rec = Serial.read();
      Serv2 = rec;
    }
    Serial.println('R');                                                      // Receive serv1 for AH in the form of character  from pi 
    while (Serial.available() == 0);
    if (Serial.available() > 0)
    {
      rec = Serial.read();
      Serv1 = rec;
    }
    Serial.println('S');                                                      // Receive trash  for AH in the form of character from pi
    while (Serial.available() == 0);
    if (Serial.available() > 0)
    {
      rec = Serial.read();
      TR = rec;
    }
    // If received char is A then AH is AH0 //
    if (AH == 'A')                                                
    {
      Pick_AH0();                                                             // Pick service for AH0
      Goto_AH0();                                                             // Goto AH0
      Place_Service();                                                        // Place service for AH0
      if (TR == 'T')                                                          // Check for trash removal service
      {
        Trash_Deposit0();                                                     // Remove trash Of AH0
      }
      else
      {
        ComeTO_Start0();                                                      // Came back to start node
      }
      j++;
    }
    // If received char is B then AH is AH1 //
    else if (AH == 'B')                                                   
    {
      Pick_AH1();                                                             // Pick service for AH1
      Goto_AH1();                                                             // Goto AH1
      Place_Service();                                                        // Place service for AH1
      if (TR == 'T')                                                          // Check for trash removal service
      {
        Trash_Deposit1();                                                     // Remove trash Of AH1
      }
      else
      {
        ComeTO_Start1();                                                      // Came back to start node
      }
      j++;
    }
    
    // If received char is C then AH is AH2 //
    else if (AH == 'C')
    {
      Pick_AH2();                                                             // Pick service for AH2
      Goto_AH2();                                                             // Goto AH2
      Place_Service();                                                        // Place service for AH2
      if (TR == 'T')                                                          // Check for trash removal service

      {
        Trash_Deposit2();                                                     // Remove trash Of AH2
      }
      else
      {
        ComeTO_Start2();                                                      // Came back to start node
      }
      j++;
    }

    // If received char is C then AH is AH2 //
    else if (AH == 'D')
    {
      Pick_AH3();                                                             // Pick service for AH3
      Goto_AH3();                                                             // Goto AH3
      Place_Service();                                                        // Place service for AH3
      if (TR == 'T')                                                          // Check for trash removal service
      {
        Trash_Deposit3();                                                     // Remove trash Of AH3
      }
      else
      {
        ComeTO_Start3();                                                      // Came back to start node
      }
      j++;
    }

  }
}



//// **** This function is used to provide service for AH0 **** //// 
void Pick_AH0(void)
{
  if (Serv1 != 'N' && Serv2 != 'N')                                         // Condition to check service 1 and service 2
  {
    Check_Array2();                                                         // Check array 2 for service 2 of AH0
    Pick_Serv2();                                                           // Pick up service 2 of AH0
    Check_Array1();                                                         // Check array 1 for service 1 of AH0
    Pick_Serv1();                                                           // Pick up service 1 of AH0
  }


  else if (Serv1 != 'N' && Serv2 == 'N')                                    // Check for service 1 only
  {
    Check_Array1();                                                         // Check array 1 for service 1 of AH0
    Pick_Serv1();                                                           // Pick up service 1 of AH0
  }


  else if (Serv1 == 'N' && Serv2 != 'N')                                    // Check for service 2 only
  {
    Check_Array2();                                                         // Check array 2 for service 2 of AH0
    Pick_Serv2();                                                           // Pick up service 2 of AH0

  }
}

//// **** This function is used to provide service for AH1 **** ////
//// Flow of function is same as for AH0 ////
void Pick_AH1(void)
{
  if (Serv1 != 'N' && Serv2 != 'N')
  {
    Check_Array2();
    Pick_Serv2();
    Check_Array1();
    Pick_Serv1();
  }


  else if (Serv1 != 'N' && Serv2 == 'N')
  {
    Check_Array1();
    Pick_Serv1();
  }


  else if (Serv1 == 'N' && Serv2 != 'N')
  {
    Check_Array2();
    Pick_Serv2();

  }
}



//// **** This function is used to provide service for AH1 **** ////
//// Flow of function is same as for AH0 ////

void Pick_AH2(void)
{
  if (Serv1 != 'N' && Serv2 != 'N')
  {
    Check_Array2();
    Pick_Serv2();
    Check_Array1();
    Pick_Serv1();
  }


  else if (Serv1 != 'N' && Serv2 == 'N')
  {
    Check_Array1();
    Pick_Serv1();
  }


  else if (Serv1 == 'N' && Serv2 != 'N')
  {
    Check_Array2();
    Pick_Serv2();

  }
}


//// **** This function is used to provide service for AH1 **** ////
//// Flow of function is same as for AH0 ////

void Pick_AH3(void)
{
  if (Serv1 != 'N' && Serv2 != 'N')
  {
    Check_Array2();
    Pick_Serv2();
    Check_Array1();
    Pick_Serv1();
  }


  else if (Serv1 != 'N' && Serv2 == 'N')
  {
    Check_Array1();
    Pick_Serv1();
  }


  else if (Serv1 == 'N' && Serv2 != 'N')
  {
    Check_Array2();
    Pick_Serv2();

  }
}

//// **** Function to traverse path to AH0 **** ////

void Goto_AH0(void)
{
  SlowRight();
  delay(900);
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  Frd();
  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
    }
  }
}


//// **** Function to traverse path to AH1 **** ////

void Goto_AH1(void)
{
  SlowRight();
  delay(900);
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  Frd();
  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to traverse path to AH2 **** ////

void Goto_AH2(void)
{
  SlowRight();
  delay(900);
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  Frd();
  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
    }
  }
}


//// **** Function to traverse path to AH3 **** ////

void Goto_AH3(void)
{
  SlowRight();
  delay(900);
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  Frd();
  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
    }
  }
}


//// **** Check array 1 for service 1 of AH **** ////

void Check_Array1(void)
{
  if (Array[0] == Serv1)
    node = 0;
  else if (Array[1] == Serv1)
    node = 1;
  else if (Array[2] == Serv1)
    node = 2;
  else if (Array[3] == Serv1)
    node = 3;
  else if (Array[4] == Serv1)
    node = 4;
  else if (Array[5] == Serv1)
    node = 5;
}


//// **** Check array 2 for service 2 of AH **** ////

void Check_Array2(void)
{
  if (Array[0] == Serv2)
    node = 0;
  else if (Array[1] == Serv2)
    node = 1;
  else if (Array[2] == Serv2)
    node = 2;
  else if (Array[3] == Serv2)
    node = 3;
  else if (Array[4] == Serv2)
    node = 4;
  else if (Array[5] == Serv2)
    node = 5;
}

//// **** Pick service 2 of AH **** ////

void Pick_Serv2(void)
{
  if (node == 0)
  {
    Goto_node0();
    full_pick();
    Comeback0();
    Array[0] = 0;
  }
  else if (node == 1)
  {
    Goto_node1();
    full_pick();
    Comeback1();
    Array[1] = 0;
  }
  else if (node == 2)
  {
    Goto_node2();
    full_pick();
    Comeback2();
    Array[2] = 0;
  }
  else if (node == 3)
  {
    Goto_node3();
    full_pick();
    Comeback3();
    Array[3] = 0;
  }
  else if (node == 4)
  {
    Goto_node4();
    full_pick();
    Comeback4();
    Array[4] = 0;
  }
  else if (node == 5)
  {
    Goto_node5();
    full_pick();
    Comeback5();
    Array[5] = 0;
  }

}


//// **** Function to go to node 0 from current location to pick up service **** ////
void Goto_node0(void)
{
  Frd();
  delay(100);
  SlowLeft();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n) {
      case 3:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to go to node 1 from current location to pick up service **** ////

void Goto_node1(void)
{
  Frd();
  delay(100);
  SlowLeft();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  n = 0;
  while (n <= 1)
  {
    Line_Follow();
    switch (n) {
      case 2:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to go to node 2 from current location to pick up service **** ////

void Goto_node2(void)
{
  Frd();
  delay(100);
  n = 0;
  SlowLeft();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  while (n != 1)
  {
    Line_Follow();
    switch (n) {
      case 1:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to go to node 3 from current location to pick up service **** ////

void Goto_node3(void)
{
  Frd();
  delay(100);
  n = 0;
  SlowRight();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  while (n != 1)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to go to node 4 from current location to pick up service **** ////

void Goto_node4(void)
{
  Frd();
  delay(100);
  n = 0;
  SlowRight();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  while (n <= 1)
  {
    Line_Follow();
    switch (n)
    {
      case 2:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to go to node 5 from current location to pick up service **** ////

void Goto_node5(void)
{
  Frd();
  delay(100);
  n = 0;
  SlowRight();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to traverse path to return position from  node 0 **** //// 

void Comeback0(void)
{
  SlowRight();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 3:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(500);
    }
  }
}

//// **** Function to traverse path to return position from  node 1 **** ////

void Comeback1(void)
{
  SlowRight();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  n = 0;
  while (n <= 1)
  {
    Line_Follow();
    switch (n)
    {
      case 2:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(500);
    }
  }
}

//// **** Function to traverse path to return position from  node 2 **** ////

void Comeback2(void)
{
  SlowRight();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  n = 0;
  while (n != 1)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(500);
    }
  }
}

//// **** Function to traverse path to return position from  node 3 **** ////

void Comeback3(void)
{
  SlowLeft();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  n = 0;
  while (n != 1)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(500);
    }
  }
}

//// **** Function to traverse path to return position from  node 4 **** ////

void Comeback4(void)
{
  SlowLeft();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  n = 0;
  while (n <= 1)
  {
    Line_Follow();
    switch (n)
    {
      case 2:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(500);
    }
  }
}

//// **** Function to traverse path to return position from  node 5 **** ////

void Comeback5(void)
{
  SlowLeft();
  MS = 0;
  while (MS <= 50)
  {
    Read();
  }
  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 3:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
        Stop();
        delay(500);
    }
  }
}

//// **** Function to trace return path from AH0 to start node **** ////
 
void ComeTO_Start0(void)
{

  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to trace return path from AH1 to start node **** ////

void ComeTO_Start1(void)
{

  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to trace return path from AH2 to start node **** ////

void ComeTO_Start2(void)
{

  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to trace return path from AH3 to start node **** ////

void ComeTO_Start3(void)
{

  n = 0;
  while (n <= 2)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to deposit trash from AH0 to TDZ **** ////

void Trash_Deposit0(void)
{

  n = 0;
  while (n <= 4)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
        SlowLeft();
        delay(300);
        servo_motor.write(0);
        delay(1000);
        SlowRight();
        delay(300);
        std_motor.write(40);
        delay(500);
        servo_motor.write(90);
        delay(1000);
        std_motor.write(4);
        delay(500);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 5:
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to deposit trash from AH1 to TDZ **** ////

void Trash_Deposit1(void)
{

  n = 0;
  while (n <= 4)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
        SlowLeft();
        delay(300);
        servo_motor.write(0);
        delay(1000);
        SlowRight();
        delay(300);
        std_motor.write(40);
        delay(500);
        servo_motor.write(90);
        delay(1000);
        std_motor.write(4);
        delay(500);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 5:
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to deposit trash from AH2 to TDZ **** ////

void Trash_Deposit2(void)
{

  n = 0;
  while (n <= 4)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
        SlowLeft();
        delay(300);
        servo_motor.write(0);
        delay(1000);
        SlowRight();
        delay(300);
        std_motor.write(40);
        delay(500);
        servo_motor.write(90);
        delay(1000);
        std_motor.write(4);
        delay(500);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 5:
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to deposit trash from AH3 to TDZ **** ////
void Trash_Deposit3(void)
{

  n = 0;
  while (n <= 4)
  {
    Line_Follow();
    switch (n)
    {
      case 1:
        Frd();
        delay(100);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 2:
        Frd();
        delay(100);
        SlowLeft();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 3:
        Stop();
        delay(1000);
        SlowLeft();
        delay(300);
        servo_motor.write(0);
        delay(1000);
        SlowRight();
        delay(300);
        std_motor.write(40);
        delay(500);
        servo_motor.write(90);
        delay(1000);
        std_motor.write(4);
        delay(500);
        SlowRight();
        MS = 0;
        while (MS <= 50)
        {
          Read();
        }
      case 5:
        Stop();
        delay(1000);
    }
  }
}

//// **** Function to place service in respective location of particular AH **** ////

void Place_Service(void)
{
  if (Serv1 != 'N' && Serv2 != 'N')
  {
    Frd();
    delay(100);
    SlowLeft();
    MS = 0;
    while (MS <= 50)
    {
      Read();
    }
    Stop();
    delay(500);
    Back();
    delay(100);
    half_place();
    SlowRight();
    MS = 0;
    while (MS <= 50)
    {
      Read();
    }
    Stop();
    delay(500);
    Back();
    delay(100);
    full_place();
  }

  else if (Serv1 == 'N' && Serv2 != 'N')
  {
    Frd();
    delay(100);
    SlowRight();
    MS = 0;
    while (MS <= 50)
    {
      Read();
    }
    Stop();
    delay(500);
    Back();
    delay(100);
    full_place();
    if (TR == 'T')
    {
      SlowLeft();
      MS = 0;
      while (MS <= 50)
      {
        Read();
      }
      Stop();
      delay(500);
      Serial.print("Y");
      delay(1000);
      Back();
      delay(100);
      half_pick();
      SlowLeft();
      MS = 0;
      while (MS <= 50)
      {
        Read();
      }
      Stop();
      delay(500);
    }
  }



  else if (Serv1 != 'N' && Serv2 == 'N')
  {
    Frd();
    delay(100);
    SlowLeft();
    MS = 0;
    while (MS <= 50)
    {
      Read();
    }
    Stop();
    delay(500);
    Back();
    delay(100);
    half_place();
    if (TR == 'T')
    {
      SlowLeft();
      MS = 0;
      while (MS <= 50)
      {
        Read();
      }
      Stop();
      delay(500);
      Serial.print("Y");
      delay(1000);
      Back();
      delay(100);
      half_pick();
      SlowLeft();
      MS = 0;
      while (MS <= 50)
      {
        Read();
      }
      Stop();
      delay(500);
    }
  }

  else if (Serv1 == 'N' && Serv2 == 'N')
  {
    Serial.println("C");
    while (Serial.available() == 0);
    if (Serial.available() > 0)
    {
      rec = Serial.read();
    }
    if (rec == 'Y')
    {
      Frd();
      delay(100);
      SlowLeft();
      MS = 0;
      while (MS <= 50)
      {
        Read();
      }
      Stop();
      delay(500);
      Back();
      delay(100);
      half_pick();
      SlowLeft();
      MS = 0;
      while (MS <= 50)
      {
        Read();
      }
      Stop();
      delay(500);
    }
    else
    {
      Frd();
      delay(100);
      SlowRight();
      MS = 0;
      while (MS <= 50)
      {
        Read();
      }
      Stop();
      delay(500);
      Serial.println("Y");
      delay(1000);
      Back();
      delay(100);
      half_pick();
      SlowRight();
      MS = 0;
      while (MS <= 50)
      {
        Read();
      }
      Stop();
      delay(500);
    }
  }

}



void Frd(void)                                                                  // Forward Function
{
  analogWrite(RE, 150);
  analogWrite(LE, 255);
  digitalWrite(RF, 1);
  digitalWrite(RB, 0);
  digitalWrite(LF, 1);
  digitalWrite(LB, 0);
}


void Left(void)                                                                // Left Function
{
  analogWrite(RE, 255);
  analogWrite(LE, 0);
  digitalWrite(RF, 1);
  digitalWrite(RB, 0);
  digitalWrite(LF, 1);
  digitalWrite(LB, 0);
}

void Right(void)                                                             // Right Function
{
  analogWrite(RE, 0);
  analogWrite(LE, 255);
  digitalWrite(RF, 1);
  digitalWrite(RB, 0);
  digitalWrite(LF, 1);
  digitalWrite(LB, 0);
}

void Stop(void)                                                             // Stop Function
{
  digitalWrite(RE, 0);
  digitalWrite(LE, 0);
  digitalWrite(RF, 0);
  digitalWrite(RB, 0);
  digitalWrite(LF, 0);
  digitalWrite(LB, 0);
}

void Back(void)                                                            // Back Function
{
  digitalWrite(RE, 1);
  digitalWrite(LE, 1);
  digitalWrite(RF, 0);
  digitalWrite(RB, 1);
  digitalWrite(LF, 0);
  digitalWrite(LB, 1);
}

void Read(void)                                                          // Read Function
{
  LS = analogRead(A0);                                                   // Left Sensor
  MS = analogRead(A1);                                                   // Middle Sensor
  RS = analogRead(A2);                                                   // Right Sensor
}

void SharpLeft(void)                                                    // Sharp Left Function
{
  analogWrite(RE, 200);
  analogWrite(LE, 200);
  digitalWrite(RF, 1);
  digitalWrite(RB, 0);
  digitalWrite(LF, 0);
  digitalWrite(LB, 1);
}


void SharpRight(void)                                                   // Sharp Right Function
{
  analogWrite(RE, 200);
  analogWrite(LE, 200);
  digitalWrite(RF, 0);
  digitalWrite(RB, 1);
  digitalWrite(LF, 1);
  digitalWrite(LB, 0);

}


void SlowRight(void)                                                  // Slow Right Function
{
  analogWrite(RE, 150);
  analogWrite(LE, 170);
  digitalWrite(RF, 0);
  digitalWrite(RB, 1);
  digitalWrite(LF, 1);
  digitalWrite(LB, 0);

}


void SlowLeft(void)                                                    // Slow Left Function
{
  analogWrite(RE, 130);
  analogWrite(LE, 170);
  digitalWrite(RF, 1);
  digitalWrite(RB, 0);
  digitalWrite(LF, 0);
  digitalWrite(LB, 1);

}




//// **** Function to full pick up the supply **** ////

void full_pick()
{
  std_motor.write(40);                                                  // open gripper jaws
  delay(1000);
  servo_motor.write(0);                                                 // take down vertical arm
  delay(1000);
  std_motor.write(4);                                                   // close gripper jaw
  delay(1000);
  servo_motor.write(150);                                               // move veritical arm up
  delay(1500);
  std_motor.write(40);                                                  // open gripper jaws
  delay(1000);
}

//// **** Function to full place up the supply **** ////

void full_place()
{
  std_motor.write(40);                                                 // open gripper jaws
  delay(1000);
  servo_motor.write(150);                                              // take up vertical arm
  delay(1200);
  std_motor.write(4);                                                  // close gripper jaw
  delay(1000);
  servo_motor.write(0);                                                // move veritical arm down
  delay(1500);
  std_motor.write(40);                                                 // open gripper jaws
  delay(1000);
}

//// **** Function to half place the supply **** ////

void half_place()
{

  servo_motor.write(0);   // move veritical arm down
  delay(1000);
  std_motor.write(40);    // open gripper jaws
  delay(1000);
}
//// **** Function to half pick up the supply **** ////

void half_pick()
{
  std_motor.write(40);    // open gripper jaws
  delay(1000);
  servo_motor.write(0);    // take down vertical arm
  delay(1000);
  std_motor.write(4);     // close gripper jaw
  delay(1000);
  servo_motor.write(90);   // move veritical arm up
  delay(1000);

}

//// **** function to pick service 1 of AH **** ////

void Pick_Serv1(void)
{
  if (node == 0)
  {
    Goto_node0();
    half_pick();
    Comeback0();
    Array[0];
  }
  else if (node == 1)
  {
    Goto_node1();
    half_pick();
    Comeback1();
    Array[1];
  }
  else if (node == 2)
  {
    Goto_node2();
    half_pick();
    Comeback2();
    Array[2];
  }
  else if (node == 3)
  {
    Goto_node3();
    half_pick();
    Comeback3();
    Array[3];
  }
  else if (node == 4)
  {
    Goto_node4();
    half_pick();
    Comeback4();
    Array[4];
  }
  else if (node == 5)
  {
    Goto_node5();
    half_pick();
    Comeback5();
    Array[5];
  }


}
