include <stdio.h>
int main(){
    int choice;
    printf("Welcome to the Adventure!\n");
    printf("1. Go left\n");
    printf("2. Go right\n");
    printf("Enter your choice:    ");
    scanf("%d", &choice);
    if (choice == 1){
        printf("You chose to go left. You encounter a monster!\n");
        printf("You can either\n");
        printf("1.Fight the monster\n");
        printf("2. Run away\n");
        printf("Enter your choice:   ");
        scanf("%d", &choice);
    
       if (choice == 1)
       {
        printf("You bravely fight the monster and defeat it!\n");
       }
     else if (choice == 2)
       {
        printf("You wisely run away from the monster!\n");
       }
     else 
       {
        printf("Invalid choice. You freeze in fear!\n");
       }
    }

    if (choice == 2)
     { 
       printf("You chose to go right. You find a trasure chest!\n");
       printf("You can either:\n");
       printf("1.Open the treasure chest\n");
       printf("2.leave it and continue exploring\n");
       printf("Enter your choice: ");
       scanf("%d", &choice);
       if (choice == 1)
        { printf("You Open the treasure chest and find a valuable artifact!\n");
        }
       else if (choice == 2)
        {
            printf("You decide to ignore the hidden path and continue forward.\n");
        }
       else 
       {
           printf ("Invalid choice. You hesitate and miss your chance!\n");
       }
    }
   return 0;
}