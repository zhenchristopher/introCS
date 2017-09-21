/* Christopher Zhen
 * cms: czhen
 * Function reads a series of years from the command line then outputs the
 * dates of Easter corresponding to those years to the command line.
 */

#include <stdio.h>
#include <assert.h>

int main(void);
int calculate_Easter_date(int year);
int zellerTest(int date, int year);


/* main: returns the date for Easter from the year read from command line
 * arguments: none, reads from command line using scanf
 * return value: string with year followed by Easter date for that year
 */

int main(void)
{
    /* Variable for both the specified year, whether
     * the in document has ended or not, and the date for Easter */
    int year, endDoc, date;
    while(1)
    {
        /* Check if at end of doc */
        endDoc = scanf("%d", &year);
        if(endDoc == EOF)
        {
            break;
        }
        else
        {
            date = calculate_Easter_date(year);
            /* Throw error for invalid date */
            if(date == 0)
            {
                fprintf(stderr, "invalid date\n");
                continue;
            }
            /* Return date */
            else
            {
                if(date < 0)
                {
                    printf("%d - March %d\n", year, date*-1);
                }
                else
                {
                    printf("%d - April %d\n", year, date);
                }
            }
        }
    }
    return 0;
}

/* calculate_Easter_date: finds a number corresponding to the date of
 * Easter for that year
 * arguments: year: the year we need to find the Easter date for
 * return value: returns an integer from - 30 to 30 representing the date 
 * of Easter
 */

int calculate_Easter_date(int year)
{
    int goldenYear, century, skippedLY, corFactor, daySun, ePact, fullMoon;
    /* Different variables corresponding to G, C, X, Z, D, E, and N from
     * Don Knuth's algorithm */
    /* return 0 if invalid date */
    if(year < 1582 || year > 39999)
    {
        return 0;
    }
    /* # years since the Metonic cycle began */
    goldenYear = (year % 19) + 1;
    /* what century year is */
    century = (year / 100) + 1;
    /* # LY before century */
    skippedLY = (3 * century / 4) - 12;
    /* correction bc moon doesn't orbit exactly 235 times in 9 years */
    corFactor = ((8 * century + 5) / 25) - 5;
    /* calculate what date is Sunday */
    daySun = (5 * year / 4) - skippedLY - 10;
    /* calc age of moon at beginning of year wrt last time it was new */
    ePact = (11 * goldenYear + 20 + corFactor - skippedLY) % 30;
    /* Epact correction */
    if(ePact == 24)
    {
        ePact++;
    }
    /* Epact correction */
    else if(ePact == 25 && goldenYear > 11)
    {
        ePact++;
    }
    /* calculate date of full moon in March */
    fullMoon = 44 - ePact;
    /* full moon correction */
    if(fullMoon < 21)
    {
        fullMoon += 30;
    }
    /* calc first Sunday after first full moon in March */
    fullMoon = fullMoon + 7 - ((daySun + fullMoon) % 7);
    if(fullMoon > 31)
    {
        /* check if Sunday */
        assert(1 == zellerTest(fullMoon - 31, year) ||
            -6 == zellerTest(fullMoon - 31, year));
        /* convert to form required for main */
        return (fullMoon - 31);
    }
    else
    {
        /* check if Sunday */
        assert(1 == zellerTest(-fullMoon, year) ||
            -6 == zellerTest(fullMoon - 31, year));
        /* convert to form required for main */
        return (-fullMoon);
    }
}

/* zellerTest: returns a number corresponding to the day of the week for a
 * date and year
 * arguments: date: date in the form used by main, year: year
 * return value: returns an integer from 0 to 6 corresponding to the day of
 * the week
 */

int zellerTest(int date, int year)
{
    /* params for Zeller's congruence */
    int day, month, yCentury, century;
    /* year of the century */
    yCentury = year % 100;
    /* zero based century */
    century = year / 100;
    if(date < 0)
    {
        day = -date;
        /* month = March */
        month = 3;
    }
    else
    {
        day = date;
        /* month = April */
        month = 4;
    }
    /* Zeller's Congruence */
    return ((day + (int) ((13 * (month + 1)) / 5) + yCentury + 
        (int) (yCentury / 4) + (int) (century / 4) - 2 * century) % 7);
}