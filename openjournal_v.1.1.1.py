from tkinter import*
from tkinter import ttk
import tkinter.messagebox
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from itertools import groupby
import pickle
import sqlite3

class OpenJournal:

    def __init__(self,root):

####=======================================================================GRAPHICS_VARIABLES===================================================####
        #WINDOW
        window_width = 1200
        window_height = 720

        #COLORS
        rose='#E83845'
        gold='#FFCE30'
        green='#12EE20'
        darkgreen='#126E20'
        blackcellphone = '#343d46'
        statsfade= '#343d46'
        lightgray='#98A2AA'
        gray = '#727473'
        darkgray='#4E6075'
        font_color='white'
        buttons_color='#343d46'
        bordercolor='black'
        
      #-------------------------------------------------------------------------VARIABLES-----------------------------------------------------------#

        #TRADES
        Stock=StringVar()
        Date=StringVar()
        Hold=IntVar()
        Risk=IntVar()
        Allocation=IntVar()
        Outcome=IntVar()
        Play=StringVar()
        EntryVAR=StringVar()
        ExitVAR=StringVar()
        Stock.set("")
        Date.set("")
        Hold.set(0)
        Risk.set(0)
        Allocation.set(0)
        Outcome.set(0)
        Play.set("")
        EntryVAR.set("")
        ExitVAR.set("")
        
        #CAPITAL
        Initial_Capital=IntVar()
        User_Capital=IntVar()
        User_Deposit=IntVar()
        User_Withdrawal=IntVar()
        Saved_Capital=IntVar()
        Saved_Deposit=IntVar()
        Saved_Withdrawal=IntVar()
        User_Equity=IntVar()
          
        #STATS
        best_play=StringVar()
        best_change=IntVar()
        worst_play=StringVar()
        worst_change=IntVar()
        hit_ratio=IntVar()
        expectancy=IntVar()
        total_gain=IntVar()
        largest_gain=IntVar()
        largest_loss=IntVar()
        average_gain=IntVar()
        average_loss=IntVar()
        longest_hold=IntVar()
        average_hold=IntVar()
        average_risk=IntVar()

        #TREEVIEW
        RowID=IntVar()
        
####======================================================================DEFINE WINDOW==============================================================####
        
        self.root = root##App WINDOW SPECS
        self.root.title("Open Journal v.1.1")
        self.root.geometry("1210x730")
        self.root.resizable(width=False,height=False)
        
####================================================================MAINFRAME (TKINTER MODULE)=======================================================####
        
        self.MainFrame = Frame(self.root,bd=5,width=window_width, height=window_height,bg= bordercolor)#ROOT FRAME 
        self.MainFrame.grid(row=0,column=0)
        
    #---------------------------------------------------------------MAINFRAME_SUBDIVISIONS------------------------------------------------------------------------------------
        ###(((HORIZONTALY Divides the 720 pixels height into two frames (DisplayFrame and ButtonsFrame). Between the frames is a divider with a tickness of 5 pixels.)))###

        displayframe_width=window_width#(1200 pixels)
        buttonsframe_width=window_width#(1200 pixels)
        displayframe_height=658#start adding here
        buttonsframe_height=55
        border_thickness=5#(sum must be 720 pixels)

        self.DisplayFrame = Frame(self.MainFrame, width = displayframe_width, height = displayframe_height)#Display Frame(1200 x 655 pixels)
        self.DisplayFrame.grid(row=0,column=0)
        self.DisplayFrame.grid_propagate(False)

        self.BorderMain = Frame(self.MainFrame, width = displayframe_width, height = border_thickness,bg= bordercolor)#Horizontal Divider (thickness=5 pixels)
        self.BorderMain.grid(row=1,column=0)
        self.BorderMain.grid_propagate(False)
        
        self.ButtonsFrame = Frame(self.MainFrame,width =  buttonsframe_width, height = buttonsframe_height, bg = gray)#Buttons Frame(1200 x 60pixels)
        self.ButtonsFrame.grid(row=2,column=0)
        self.ButtonsFrame.grid_propagate(False)
        
    #---------------------------------------------------------------DISPLAYFRAME_SUBDIVISIONS---------------------------------------------------------------#
        ###(((HORIZONTALY Divides the 655 pixels height into two frames (DataFrame and SearchFrame). Between the frames is a divider with a tickness of 5 pixels.)))###
        
        dataframe_height=500#start adding here
        display_border=5
        searchframe_height=152#(sum must be 655 pixels)

        self.DataFrame = Frame(self.DisplayFrame, width = displayframe_width, height = dataframe_height)#DataFrame(1200 x 500 pixels)
        self.DataFrame.grid(row=0,column=0)
        self.DataFrame.grid_propagate(False)

        self.BorderMain = Frame(self.DisplayFrame, width = displayframe_width, height = display_border,bg= bordercolor)#Horizontal Divider (thickness=5 pixels)
        self.BorderMain.grid(row=1,column=0)
        self.BorderMain.grid_propagate(False)
        
        self.SearchFrame = Frame(self.DisplayFrame, width =  buttonsframe_width, height = searchframe_height, bg='white')#SearchFrame(1200 x 150 pixels)
        self.SearchFrame.grid(row=2,column=0)
        self.SearchFrame.grid_propagate(False)
        
    #------------------------------------------------------------DATAFRAME_SUBDIVISIONS---------------------------------------------------------------------#
        ###(((VERTICALY Divides 1200 width into three frames(Left, Mid, and Right). Between the frames are dividers with tickness of 5 pixels. (2 dividers total))))###

        left_width=258#start adding here
        right_width=258
        dataframe_border=5#(consumes twice pixels as there are two of dividers used with 5 pixels each)
        mid_width=674#(sum must be 1200 pixels)

        self.Left = Frame (self.DataFrame, width = left_width, height =  dataframe_height, bg = blackcellphone)#Left frame
        self.Left.grid(row=0,column=0)
        self.Left.grid_propagate(False)

        self.DataBorder01 = Frame (self.DataFrame, width = dataframe_border, height =  dataframe_height, bg = bordercolor)#Vertical Divider (thickness=5 pixels)
        self.DataBorder01.grid(row=0,column=1)
        self.DataBorder01.grid_propagate(False)
        
        self.Mid = Frame (self.DataFrame, width = mid_width, height =  dataframe_height, bg = blackcellphone)#Mid frame
        self.Mid.grid(row=0,column=2)
        self.Mid.grid_propagate(False)

        self.DataBorder02 = Frame (self.DataFrame, width = dataframe_border, height =  dataframe_height, bg = bordercolor)#Vertical Divider (thickness=5 pixels)
        self.DataBorder02.grid(row=0,column=3)
        self.DataBorder02.grid_propagate(False)
        
        self.Right = Frame (self.DataFrame, width = right_width, height =  dataframe_height, bg = blackcellphone)#Right frame
        self.Right.grid(row=0,column=4)
        self.Right.grid_propagate(False)

####========================================================DATABASE_MANAGEMENT (SQLITE3)=========================================####

        def TradeData():#CREATE Table
            con=sqlite3.connect("Trades.db")
            cur=con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Trades(id INTEGER PRIMARY KEY,\
                        Stock text,Date text,Hold text,Risk text,Allocation text,Outcome text,Play text,EntryVAR text,ExitVAR text)")
            con.commit()
            con.close()


        def addTrade(Stock,Date,Hold,Risk,Allocation,Outcome,Play,EntryVAR,ExitVAR):#ADD Entries to the Table
            con=sqlite3.connect("Trades.db")
            cur=con.cursor()
            cur.execute("INSERT INTO Trades VALUES (NULL,?,?,?,?,?,?,?,?,?)",(Stock,Date,Hold,Risk,Allocation,Outcome,Play,EntryVAR,ExitVAR))
            con.commit()
            con.close()

            
        def viewTrades():#RETRIEVE ALL Table Entries
            con=sqlite3.connect("Trades.db")
            cur=con.cursor()
            cur.execute("SELECT * FROM Trades")
            rows = cur.fetchall()
            con.close()
            return rows


        def searchTrade(Stock="",Date="",Hold="",Risk="",Allocation="",Outcome="",Play="",EntryVAR="",ExitVAR=""):#RETRIEVE Rows Base on User Query
            con=sqlite3.connect("Trades.db")
            cur=con.cursor()
            cur.execute("SELECT * FROM Trades WHERE Stock=? OR Date=? OR Hold=? OR Risk=? OR Allocation=? OR Outcome=? OR Play=? OR EntryVAR=? OR ExitVAR=?",\
                        (Stock,Date,Hold,Risk,Allocation,Outcome,Play,EntryVAR,ExitVAR) )
            rows = cur.fetchall()   
            con.close()
            return rows
         
            
        def updateTrade(id,Stock,Date,Hold,Risk,Allocation,Outcome,Play,EntryVAR,ExitVAR):#CHANGE Row Entry(s)
            con=sqlite3.connect("Trades.db")
            cur=con.cursor()
            cur.execute("UPDATE Trades SET Stock=?, Date=?, Hold=?, Risk=?, Allocation=?, Outcome=?, Play=?, EntryVAR=?, ExitVAR=? WHERE id=?",\
                        (Stock,Date,Hold,Risk,Allocation,Outcome,Play,EntryVAR,ExitVAR,id,))
            con.commit()
            con.close()

        def formatTable():#DELETE Entire Table
            con=sqlite3.connect("Trades.db")
            cur=con.cursor()
            cur.execute("DELETE FROM Trades " )
            con.commit()
            con.close()
        
####===================================================================BUTTON_ALGORITHMS====================================================####

        def AddTrade():##ADD row in User Database of Trades
            try:
                if(len(Stock.get())!=0):
                    addTrade(Stock.get(),Date.get(),Hold.get(),Risk.get(),Allocation.get(),Outcome.get(),Play.get(),EntryVAR.get(),ExitVAR.get())
                    tkinter.messagebox.showinfo(title="Trade Recorded",message="Your trade was successfully recorded.")
                    for row in self.tree.get_children():
                        self.tree.delete(row)
                        
                    i=0##SHOW all recorded trades
                    for row in viewTrades():
                        self.tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
                        i=i+1
                else:
                    tkinter.messagebox.showinfo(title="Invalid Input",message="Please enter stock name.")
                Refresh()#Recalculate Graphs and Stats (now including the recently added trade)
                
            except:
                tkinter.messagebox.showinfo(title="Format Not Supported",message="Please use numeric characters only for amount.")


        def SearchTrade():##SHOW rows from User Database of Trades

            ##SHOW only specified stock/play/date
            if(len(Stock.get())!=0) or (len(Play.get())!=0)\
                                    or (len(Date.get())!=0)\
                                    or (Hold.get()!=0)\
                                    or (Risk.get()!=0)\
                                    or (Allocation.get()!=0)\
                                    or (Outcome.get()!=0)\
                                    or (len(EntryVAR.get())!=0)\
                                    or (len(ExitVAR.get())!=0):
                # or (Hold.get()!="")\
                # or (Risk.get()!="")\
                # or (Allocation.get()!="")\
                # or (Outcome.get()!="")\
                
                for row in self.tree.get_children():
                    self.tree.delete(row)
                i=0
                for row in searchTrade(Stock.get(),Date.get(),Hold.get(),Risk.get(),Allocation.get(),Outcome.get(),Play.get(),EntryVAR.get(),ExitVAR.get()):
                    self.tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
                    i=i+1

            else:##SHOW all entries (if the user did not specify a Stock to search)
                for row in self.tree.get_children():
                    self.tree.delete(row)
                i=0
                for row in viewTrades():
                    self.tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
                    i=i+1 


        def Clear():##CLEARS Entry fields
            Stock.set("")
            Date.set("")
            Hold.set(0)
            Risk.set(0)
            Allocation.set(0)
            Outcome.set(0)
            Play.set("")
            EntryVAR.set("")
            ExitVAR.set("")
                
            
        def VariableDefaults():##RESET ALL variables to default
            Stock.set("")
            Date.set("")
            Hold.set(0)
            Risk.set(0)
            Allocation.set(0)
            Outcome.set(0)
            Play.set("")
            EntryVAR.set("")
            ExitVAR.set("")

            Saved_Capital.set(0)
            Saved_Deposit.set(0)
            Saved_Withdrawal.set(0)
            User_Capital.set(0)
            User_Deposit.set(0)
            User_Withdrawal.set(0)
            Initial_Capital.set(0)
            User_Equity.set(0)

            best_play.set("")
            best_change.set(0)
            worst_play.set("")
            worst_change.set(0)
            hit_ratio.set(0)
            expectancy.set(0)
            total_gain.set(0)
            largest_gain.set(0)
            average_gain.set(0)
            largest_loss.set(0)
            average_loss.set(0)
            longest_hold.set(0)
            average_hold.set(0)
            average_risk.set(0)

                    
        def UpdateTrade():##REPLACE the Items in row in the Database with values in the Entry Field.

            try:
                selectedRow=self.tree.focus()
                RowDATA=self.tree.item(selectedRow)
                RowVALUES=RowDATA["values"]
                ACTIVERowID=RowVALUES[0]
                RowID.set(int(ACTIVERowID))
                
                updateTrade(RowID.get(),Stock.get(),Date.get(),Hold.get(),Risk.get(),Allocation.get(),Outcome.get(),Play.get(),EntryVAR.get(),ExitVAR.get())
                for row in self.tree.get_children():
                    self.tree.delete(row)
                i=0
                for row in viewTrades():
                    self.tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
                    i=i+1
                tkinter.messagebox.showinfo(title="Update Successful",message="Row entires has been succesfully updated.")
            except:
                pass#IGNORE command to Update Trade if Treeview is Empty

            
            Refresh()
            
            
        def FormatTable():##CLEAR ALL stored values
            try:
                FormatJournal=tkinter.messagebox.askyesno("Full Reset","Click YES if you want to DELETE ALL records.")
                if FormatJournal>0:
                    formatTable()
                    for row in self.tree.get_children():
                        self.tree.delete(row)
                    VariableDefaults()
                    currentCAPITAL=Saved_Capital.get()##SET currentCAPITAL value to zero
                    pickle_Out_currentCAPITAL=open("int.pickle","wb")
                    pickle.dump(currentCAPITAL,pickle_Out_currentCAPITAL)
                    
                    Refresh()
                    
                    tkinter.messagebox.showinfo(title="Full Reset Successful",message="All records were successfully deleted.")
                    return
            except:
                tkinter.messagebox.showinfo(title="Full Reset Failed",message="Database was not successfully cleared.")
                
                                                         
        def ExitJournal():#SAVE variables and EXIT program
            currentCAPITAL=Saved_Capital.get()##SAVE Current Capital calculations
            pickle_Out_currentCAPITAL=open("int.pickle","wb")
            pickle.dump(currentCAPITAL,pickle_Out_currentCAPITAL)
            

            ExitJournal=tkinter.messagebox.askyesno("Save and Exit?","Your work has been saved. \n \nDo you want to exit too?")
            if ExitJournal>0:
                root.destroy()
                return

    #--------------------------------------------------------CAPITAL MANAGEMENT--------------------------------------------------#

        def Set_SavedVAR():##SET current user capital equal to its value during last exit.
            try:
                pickle_In_currentCAPITAL=open("int.pickle","rb")##RETRIEVE first user capital from last session
                currentCAPITAL=pickle.load(pickle_In_currentCAPITAL)
                Saved_Capital.set(currentCAPITAL)
                pickle_In_currentCAPITAL.close()
                PlotEquity()
            except:
                Saved_Capital.set(0)
                

        def Lock_Capital():##SET INITIAL capital
            User_Deposit.set(0)
            User_Withdrawal.set(0)
            if (Saved_Capital.get()==0):
                if (User_Capital.get()>0):
                    i=User_Capital.get()
                    Saved_Capital.set(i)
                    Refresh()#Recalculate Stats and Chart (this time with Initial Capital included)
                    tkinter.messagebox.showinfo(title="Initial Capital Saved",message="Equity Values had been Recalcuted.")    
            else:
                tkinter.messagebox.showinfo(title="Format Not Supported",message="Entries must be numeric only.")
                
            PlotEquity()#REDRAW Chart (with Initial Capital Included)
                            

        def Lock_Deposit():##ADD new DEPOSITS
            User_Capital.set(0)
            User_Withdrawal.set(0)
            if (Saved_Capital.get()>0):
                if (User_Deposit.get()>0):
                    s=Saved_Capital.get()
                    d=User_Deposit.get()
                    total=s+d
                    Saved_Capital.set(total)

                    Refresh()#Recalculate Stats and Chart (with recently added deposits)
                    tkinter.messagebox.showinfo(title="Deposit Recorded",message="New Deposit has been factored in calculations.")   
            User_Deposit.set(0)


        def Lock_Withdrawal():##SUBTRACT Withdrawals
            User_Capital.set(0)
            User_Deposit.set(0)
            if (User_Withdrawal.get()>0):
                if (Saved_Capital.get()>0):
                    s=Saved_Capital.get()
                    w=User_Withdrawal.get()
                    difference=s-w
                    Saved_Capital.set(difference)
                    
                    Refresh()#Recalculate Stats and Chart
                    tkinter.messagebox.showinfo(title="Withdrawal Recorded",message="Withdrawal is now included in chart calculation.")    
            User_Withdrawal.set(0)

    #--------------------------------------------------------MATH FUCTIONS--------------------------------------------------#
                
        def MATH_TotalGain():
            allGain=viewTrades()##CREATE a list of all OUTCOMES
            Outcomeslist=[]
            for row in allGain:
                Outcomeslist.append(row[6])

            Total_Gain=0##ADD all OUTCOMES
            for outcome in Outcomeslist:
                y=Total_Gain+int(outcome)
                Total_Gain=y
                
            total_gain.set(Total_Gain)##SET 'Total Gain' Equal to the Sum
            return Total_Gain 


        def MATH_AverageRisk():
            allrisk=viewTrades()#CREATE a list of all RISK
            blankRisklist=[]
            for row in allrisk:
                blankRisklist.append(row[4])
                  
            totalRisk=0##ADD all RISK
            for risk in blankRisklist:
                y=totalRisk+int(risk)
                totalRisk=y
                
            IDlist=TradeIDsList()##GET the AVERAGE
            tradeCount=len(IDlist)
            if tradeCount>0:
                averageRisk=int(totalRisk/tradeCount)
            else:
                averageRisk=0
            
            average_risk.set(averageRisk)#SET 'Average Risk' equal to the Average
            return averageRisk

    
        def MATH_AverageHold():
            allHold=viewTrades()##CREATE a list of all HOLDING Periods
            blankHoldlist=[]
            for row in allHold:
                blankHoldlist.append(row[3])
                  
            totalHold=0##ADD all holding periods
            for hold in blankHoldlist:
                y=totalHold+int(hold)
                totalHold=y
                
            IDlist=TradeIDsList()##AVERAGE all holding periods
            tradeCount=len(IDlist)
            if tradeCount>0:
                averageHold=int(totalHold/tradeCount)
            else:
                averageHold=0
            average_hold.set(averageHold)#SET 'Average Hold' equal to the Average
            return averageHold
            

        def MATH_AverageGain():
            allGain=viewTrades()##CREATE a list of all GAINS
            blankGainlist=[]
            for row in allGain:
                blankGainlist.append(row[6])
                
            totalGain=0##GET the total of all GAINS
            gainCount=0
            for gain in blankGainlist:
                gainINT=int(gain)
                if gainINT>0:
                    y=totalGain+int(gain)
                    totalGain=y
                    gainCount+=1

            IDlist=TradeIDsList()##AVERAGE all GAINS
            gainCount=len(IDlist)
            if gainCount>0:
                averageGain=int(totalGain/gainCount)
            else:
                averageGain=0
                
            average_gain.set(averageGain)#SET 'Average Gain' equal to the Average
            return averageGain


        def MATH_AverageLoss():
            allLoss=viewTrades()##CREATE a list of all LOSSES
            blankLosslist=[]
            for row in allLoss:
                blankLosslist.append(row[6])
                
            totalLoss=0##ADD all LOSSES
            lossCount=0
            for loss in blankLosslist:
                lossINT=int(loss)
                if lossINT<0:
                    y=totalLoss+int(loss)
                    totalLoss=y
                    lossCount+=1

            IDlist=TradeIDsList()##AVERAGE all LOSSES
            if lossCount>0:
                averageLoss=int(totalLoss/lossCount)
            else:
                averageLoss=0
                
            average_loss.set(averageLoss)#SET 'Average Loss' equal to the Average
            return averageLoss


        def MATH_LargestGain():
            allGain=viewTrades()##CREATE a list of all GAINS
            Outcomeslist=[]
            for row in allGain:
                Outcomeslist.append(row[6])
                
            OutcomeslistINT=[]##CONVERT all entries into Integers
            for outcome in Outcomeslist:
                outcomeINT=int(outcome)
                OutcomeslistINT.append(outcomeINT)
   
            OutcomeslistINT.sort()##GET the largest GAIN
            if len(OutcomeslistINT)>0:
                LargestGain=OutcomeslistINT[(len(OutcomeslistINT))-1]
            else:
                LargestGain=0
            largest_gain.set(LargestGain)#SET 'Largest Gain' equal to the largest gain
            return LargestGain
                

        def MATH_LargestLoss():
            allGain=viewTrades()##CREATE a list of all LOSSES
            Outcomeslist=[]
            for row in allGain:
                Outcomeslist.append(row[6])
                
            OutcomeslistINT=[]##CONVERT all entries into Integers
            for outcome in Outcomeslist:
                outcomeINT=int(outcome)
                OutcomeslistINT.append(outcomeINT)
   
            OutcomeslistINT.sort()##GET the largest LOSS
            if len(OutcomeslistINT)>0:
                LargestLoss=OutcomeslistINT[0]
            else:
                LargestLoss=0
                
            largest_loss.set(LargestLoss)#SET 'Largest Loss' equal to the largest loss
            return LargestLoss


        def MATH_LongestHold():
            allHold=viewTrades()##CREATE a list of all HOLDING PERIODS
            Holdlist=[]
            for row in allHold:
                Holdlist.append(row[3])

            HoldlistINT=[]##CONVERT all entries into INT
            for hold in Holdlist:
                holdINT=int(hold)
                HoldlistINT.append(holdINT)
   
            HoldlistINT.sort()##GET the longest holding period
            if len(HoldlistINT)>0:
                LongestHold=HoldlistINT[(len(HoldlistINT))-1]
            else:
                LongestHold=0
                
            longest_hold.set(LongestHold)#SET 'Longest Hold' equal to the longest holding period
            return LongestHold
        

        def MATH_HitRatio():
            allGain=viewTrades()##CREATE a list of all OUTCOMES
            Outcomeslist=[]
            for row in allGain:
                Outcomeslist.append(row[6])

            Gain_Count=0##COUNTS Number of WINS and LOSSES
            Loss_Count=0
            for outcome in Outcomeslist:
                outcomeINT=int(outcome)
                if outcomeINT>0:
                    Gain_Count=Gain_Count+1
                else:
                    Loss_Count=Loss_Count+1

            Total_Count=Gain_Count+Loss_Count##CALCULATE the hit ratio
            if Total_Count>0:
                HitRatio=int((Gain_Count/Total_Count*100))
            else:
                HitRatio=0
                
            hit_ratio.set(HitRatio)#SET 'Hit Ratio' equal to hit ratio
            return HitRatio
        

        def MATH_Expectancy():
            Hitratio=MATH_HitRatio()#START retreiving CALCULATIONS from Previously Defined Functions
            Missratio=100-Hitratio
            Avegain=MATH_AverageGain()
            Aveloss=MATH_AverageLoss()

            Expectancy=int(((Hitratio*Avegain)-(Missratio*Aveloss))/100)##CALCULATE expectancy
            expectancy.set(Expectancy)
            return Expectancy
                
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@_SUPER ALGORITHM_START_@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
        
        ###(((Has 4 Outputs namely, "BEST PLAY", "BEST PLAY PORT CHANGE", "WORST PLAY", "WORST PLAY PORT CHANGE")))###

        def MATH_PlayANALYSIS():
            allTrades=viewTrades()#Retrieve the entries in the tradesDatabase in a form of an list
            if (len(allTrades)>0):#Checks if the Database is not empty
                RepPlayslist=[]##CREATE a list of user plays WITH REPETITION
                for row in allTrades:
                    RepPlayslist.append(row[7])
                UniqPlayLIST=set(RepPlayslist)#REMOVE DUPLICATE user plays

                PlayWithExpectancyLIST=[]##RECORD tuples in the format: ({User Play}, {Its Expectancy})
                for play in UniqPlayLIST:
                    win_count=0
                    loss_count=0
                    win_total=0
                    loss_total=0
                    for row in allTrades:
                        if (play==row[7]):
                            if (int(row[6])>0):
                                win_count+=1
                                win_total+=int(row[6])
                            else:
                                loss_count+=1
                                loss_total+=int(row[6])
                    total_count=win_count+loss_count##CALCULATE Expectancy 
                    if (win_count!=0):#PREVENT Zero Division Error
                        win_ratio=win_count/total_count
                        average_win=win_total/win_count
                    else:
                        win_ratio=0
                        average_win=0
                    if (loss_count!=0):
                        loss_ratio=loss_count/total_count
                        average_loss=loss_total/loss_count
                    else:
                        loss_ratio=0
                        average_loss=0 
                    expectancy=(win_ratio*average_win)+(loss_ratio*average_loss)
                    PlayWithExpectancyLIST.append((play,expectancy))

                
                PlayEx_LEN=len(PlayWithExpectancyLIST)##SORT PLAYs by its expentancy
                for i in range(0, PlayEx_LEN):
                    for j in range(0,PlayEx_LEN-i-1):
                        if (PlayWithExpectancyLIST[j][1]>PlayWithExpectancyLIST[j+1][1]):
                            tempo = PlayWithExpectancyLIST[j]
                            PlayWithExpectancyLIST[j]=PlayWithExpectancyLIST[j+1]
                            PlayWithExpectancyLIST[j+1]=tempo
                            
                BestPlayTUPLE=PlayWithExpectancyLIST[len(PlayWithExpectancyLIST)-1]#OBTAIN and SET 'Best Play' Value
                BestPlayVALUE=BestPlayTUPLE[0]
                best_play.set(BestPlayVALUE)
                
                WorstPlayTUPLE=PlayWithExpectancyLIST[0]##OBTAIN and SET 'Worst Play' Value
                WorstPlayVALUE=WorstPlayTUPLE[0]
                worst_play.set(WorstPlayVALUE)

                bestplay_portchange=0##CALCULATE and SET Best Play Port Change Value
                for row in allTrades:
                    if (BestPlayVALUE==row[7]):
                        bestplay_portchange+=int(row[6])
                best_change.set(bestplay_portchange)
          
                worstplay_portchange=0##CALCULATE and SET Worst Play Port Change Value
                for row in allTrades:
                    if (WorstPlayVALUE==row[7]):
                        worstplay_portchange+=int(row[6])
                worst_change.set(worstplay_portchange)         
  
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@_SUPER ALGORITHM_END_@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

#--------------------------------------------------------GRAPHING FUCTIONS--------------------------------------------------#

        def TradeIDsList():##CREATE a list of IDs (will be used in plotting the X-AXIS later)
            t=viewTrades()
            IDs=[]
            for row in t:
                IDs.append(row[0])
            return(IDs)


        def OutcomeList():##CREATE a list of OUTCOMES (will in used calculation in the next function)
            o=viewTrades()
            Outcomes=[]
            for row in o:
                Outcomes.append(row[6])
            return(Outcomes)
        

        def CummulativeGainList():#CREATE a list of CUMMULATIVE GAINS (will be used in plotting the Y-AXIS later)
            tradeGains=OutcomeList()
            CumGains=[]
            Equity=Saved_Capital.get()

            for gain in tradeGains:
                y=Equity+int(gain)
                Equity=y
                CumGains.append(y)
            if (len(CumGains)>0):
                User_Equity.set(CumGains[len(CumGains)-1])
                return CumGains
            else:
                return CumGains
                

        def PlotEquity():##PLOT user EQUITY

            
            x=[0]##Include zero in the X-AXIS
            x.extend(TradeIDsList())
            
            capital_funcVar=Saved_Capital.get()##Include the Initial Capital in the Y-AXIS
            y=[]
            y.append(capital_funcVar)
            c=CummulativeGainList()
            if (len(c)>0):
                y.extend(CummulativeGainList())
            
            matplotlib.use("TkAgg")##CREATE a blank canvas
            fig=Figure(figsize=(6.74,5),dpi=100,facecolor=lightgray,frameon=True)
            equityCurve=fig.suptitle('EQUITY CURVE',fontweight='bold',fontsize=12)
            equityCurve=fig.add_subplot(111)
            
            ##PROCESS the Chart and its elements
            equityCurve.plot(x,y,color=gold,marker="o",markersize=4,markerfacecolor=gold,markeredgecolor=rose,markeredgewidth=1)
            equityCurve.set_xlabel("TRADES")
            equityCurve.set_title("Your Journey",size=12)
            equityCurve.set_facecolor(blackcellphone)
            #NOTE: axis-ticks is set to auto as tick labels get compressed as number of trades recorded increases
            
            ##SHOW the Chart and its elements to the User
            canvas=FigureCanvasTkAgg(fig,self.Mid)
            canvas.get_tk_widget().grid(row=0,column=0)

    #--------------------------------------------------------SPECIAL FUCTIONS--------------------------------------------------#

        def Refresh():##Calculates all Stats and ReDraw Chart {ORDERED recalculation. Do NOT rearrange.}
            MATH_TotalGain()
            MATH_AverageRisk()
            MATH_AverageHold()
            MATH_AverageGain()
            MATH_AverageLoss()
            MATH_HitRatio()
            MATH_LargestGain()
            MATH_LargestLoss()
            MATH_LongestHold()
            MATH_Expectancy()
            MATH_PlayANALYSIS()
    
            PlotEquity()

####============================================================TREEVIEW======================================================####
        ###Displays Search Results in table format.###

        self.tree=ttk.Treeview(self.SearchFrame, height=6)##MAKE tkinter TREE
        self.tree.grid(row=0,column=0,sticky='nsew')
        self.tree['show']='headings'
        
        self.s=ttk.Style(self.SearchFrame)##DESIGN tree HEADING
        self.s.theme_use("clam")
        self.s.configure(".",font=('Helvetica',12),height=12)
        self.s.configure("Treeview.Heading",foreground=rose,font=('Helvetica',12,"bold"))

        ##DEFINE Tree heading
        self.tree["columns"]=("ID","STOCK","DATE","HOLD","RISK","ALLOCATION","OUTCOME","PLAY","ENTRY","EXIT")
        self.tree.column("ID",anchor=CENTER,stretch=NO,width=100)
        self.tree.heading("ID",text="ID")
        self.tree.column("STOCK",anchor=CENTER,stretch=NO,width=101)
        self.tree.heading("STOCK",text="Stock")
        self.tree.column("DATE",anchor=CENTER,stretch=NO,width=140)
        self.tree.heading("DATE",text="Date")
        self.tree.column("HOLD",anchor=CENTER,stretch=NO,width=100)
        self.tree.heading("HOLD",text="Hold")
        self.tree.column("RISK",anchor=CENTER,stretch=NO,width=150)
        self.tree.heading("RISK",text="Risk")
        self.tree.column("ALLOCATION",anchor=CENTER,stretch=NO,width=140)
        self.tree.heading("ALLOCATION",text="Allocation")
        self.tree.column("OUTCOME",anchor=CENTER,stretch=NO,width=130)
        self.tree.heading("OUTCOME",text="Outcome")
        self.tree.column("PLAY",anchor=CENTER,stretch=NO,width=100)
        self.tree.heading("PLAY",text="Play")
        self.tree.column("ENTRY",anchor=CENTER,stretch=NO,width=110)
        self.tree.heading("ENTRY",text="Entry")
        self.tree.column("EXIT",anchor=CENTER,stretch=NO,width=110)
        self.tree.heading("EXIT",text="Exit")
        
        ##Make Treeview Scrollble
        self.scrollbar=ttk.Scrollbar(self.SearchFrame, orient="vertical",command=self.tree.yview)
        self.scrollbar.grid(row=0,column=1,sticky='ns')
        self.tree.configure(yscrollcommand=self.scrollbar.set,selectmode='browse')

        #--------------------------------------------------------INPUT_WIDGETS--------------------------------------------------#
            #(Back to TKINTER Display Module)
        
        padxLABEL=9#Label padding
        padxBUTTON=9#Button padding
        Left_width=11#Length of the Input Box in Characters

        ##Displays the word "STOCK" and an Input Field next to it.
        self.labelSTOCK = Label(self.Left, text = "STOCK", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelSTOCK.grid(row=0, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.entrySTOCK = Entry(self.Left, width=Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=Stock)
        self.entrySTOCK.grid(row=0, column=1, padx=5, pady=2.5)

        ##Displays the word "DATE" and an Input Field next to it.
        self.labelDATE = Label(self.Left, text = "DATE", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelDATE.grid(row=1, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.entryDATE = Entry(self.Left, width= Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=Date)
        self.entryDATE.grid(row=1, column=1, padx=5, pady=2.5)

        ##Displays the word "HOLD" and an Input Field next to it.
        self.labelHOLD = Label(self.Left, text = "HOLD", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelHOLD.grid(row=2, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.entryHOLD = Entry(self.Left, width= Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=Hold)
        self.entryHOLD.grid(row=2, column=1, padx=5, pady=2.5)

        ##Displays the word "RISK" and an Input Field next to it.
        self.labelRISK = Label(self.Left, text = "RISK", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelRISK.grid(row=3, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.entryRISK = Entry(self.Left, width=Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=Risk)
        self.entryRISK.grid(row=3, column=1, padx=5, pady=2.5)

        ##Displays the word "ALLOCATION" and an Input Field next to it.
        self.labelALLOCATION = Label(self.Left, text = "ALLOCATION", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelALLOCATION.grid(row=4, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.entryALLOCATION = Entry(self.Left, width=Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=Allocation)
        self.entrySTOCK.grid(row=0, column=1, padx=5, pady=2.5)
        self.entryALLOCATION.grid(row=4, column=1, padx=5, pady=2.5)

        ##Displays the word "OUTCOME" and an Input Field next to it.
        self.labelOUTCOME = Label(self.Left, text = "OUTCOME", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelOUTCOME.grid(row=5, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.entryOUTCOME = Entry(self.Left, width= Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=Outcome)
        self.entryOUTCOME.grid(row=5, column=1, padx=5, pady=2.5)

        ##Displays the word "PLAY" and an Input Field next to it.
        self.labelPLAY = Label(self.Left, text = "PLAY", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelPLAY.grid(row=6, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.entryPLAY = Entry(self.Left, width= Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=Play)
        self.entryPLAY.grid(row=6, column=1, padx=5, pady=2.5)

        ##Displays the word "ENTRY" and an Input Field next to it.
        self.labelENTRY = Label(self.Left, text = "ENTRY", font = ('Helvetica', 12, 'bold'), fg=gold,bg=blackcellphone )
        self.labelENTRY.grid(row=7, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.entryENTRY = Entry(self.Left, width= Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=EntryVAR)
        self.entryENTRY.grid(row=7, column=1, padx=5, pady=2.5)

        ##Displays the word "EXIT" and an Input Field next to it.
        self.labelEXIT = Label(self.Left, text = "EXIT", font = ('Helvetica', 12, 'bold'), fg=gold,bg=blackcellphone )
        self.labelEXIT.grid(row=8, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.entryEXIT = Entry(self.Left, width= Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=ExitVAR)
        self.entryEXIT.grid(row=8, column=1, padx=5, pady=2.5)

        #Spacing
        self.labelNOTHING = Label(self.Left, text = "", font = ('Helvetica', 4, 'bold'), fg=gray,bg=blackcellphone )#DividingLine
        self.labelNOTHING.grid(row=9, column=0,columnspan=2)

         #Spacing
        self.labelNOTHING = Label(self.Left, text = "", font = ('Helvetica', 2, 'bold'), fg=gray,bg=blackcellphone )#DividingLine
        self.labelNOTHING.grid(row=10, column=0,columnspan=2)
        
        ##Displays the word "INITIAL" and an Input Field next to it.
        self.labelCAPITAL = Button(self.Left, text = "INITIAL", font = ('Helvetica', 11, 'bold'), fg=blackcellphone, bg=gold,width=12,command=Lock_Capital)
        self.labelCAPITAL.grid(row=11, column=0, padx=padxBUTTON , pady=0 , sticky = 'W') 
        self.entryCAPITAL = Entry(self.Left, width= Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=User_Capital)
        self.entryCAPITAL.grid(row=11 , column=1, padx=3, pady=2.5)

        #Spacing
        self.labelNOTHING = Label(self.Left, text = "",font = ('Helvetica', 4, 'bold'), bg=blackcellphone)#InvisibleTextforSpacing
        self.labelNOTHING.grid(row=12, column=0,columnspan=2)

        ##Displays the word "DEPOSIT" and an Input Field next to it.
        self.labelDEPOSIT = Button(self.Left, text = "DEPOSIT", font = ('Helvetica', 11, 'bold'), fg=font_color, bg=darkgreen,width=12,command=Lock_Deposit)
        self.labelDEPOSIT.grid(row=13, column=0, padx=padxBUTTON , pady=0 , sticky = 'W') 
        self.entryDEPOSIT = Entry(self.Left, width= Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=User_Deposit)
        self.entryDEPOSIT.grid(row=13 , column=1, padx=3, pady=2.5)

        #Spacing
        self.labelNOTHING = Label(self.Left, text = "",font = ('Helvetica', 4, 'bold'), bg=blackcellphone)#InvisibleTextforSpacing
        self.labelNOTHING.grid(row=14, column=0,columnspan=2)

        ##Displays the word "WITHDRAWAL" and an Input Field next to it.
        self.labelWITHDRAWAL = Button(self.Left, text = "WITHDRAWAL", font = ('Helvetica', 11, 'bold'), fg=font_color, bg=rose,width=12,command=Lock_Withdrawal)
        self.labelWITHDRAWAL.grid(row=15, column=0, padx=padxBUTTON , pady=0 , sticky = 'W') 
        self.entryWITHDRAWAL = Entry(self.Left, width= Left_width, font = ('Helvetica', 12, 'bold'),justify=CENTER,text=User_Withdrawal)
        self.entryWITHDRAWAL.grid(row=15 , column=1, padx=3, pady=2.5)

        #Spacing
        self.labelNOTHING = Label(self.Left, text = "",font = ('Helvetica', 4, 'bold'), bg=blackcellphone)#InvisibleTextforSpacing
        self.labelNOTHING.grid(row=16, column=0,columnspan=2)

        ##Displays the Words "CAPITAL" and its equivalent value.
        self.labelCAP = Label(self.Left, text = "CAPITAL", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone)
        self.labelCAP.grid(row=17, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.labelCAPValue = Label(self.Left, textvariable=Saved_Capital, font = ('Helvetica', 12, 'bold'), width = 10, fg=font_color,bg=darkgray )
        self.labelCAPValue.grid(row=17, column=1, padx=4, pady=2.5, sticky = 'W')

        ##Displays the Words "EQUITY" and its equivalent value.
        self.labelEQ = Label(self.Left, text = "EQUITY", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone)
        self.labelEQ.grid(row=18, column=0, padx=padxLABEL, pady=2.5, sticky = 'W')
        self.labelEQValue = Label(self.Left, textvariable=User_Equity, font = ('Helvetica', 12, 'bold'), width = 10, fg=font_color,bg=darkgray)
        self.labelEQValue.grid(row=18, column=1, padx=4, pady=2.5, sticky = 'W')

        #--------------------------------------------------------------------USER STATS-------------------------------------------------------------------------------#

        midwidth = 11 #whitespace given to label values
        
        #Spacing
        self.labelNOTHING = Label(self.Right, text = "",font = ('Helvetica', 4, 'bold'), bg=blackcellphone)#InvisibleTextforSpacing
        self.labelNOTHING.grid(row=0, column=0)

        ###PLAY#####
        padxVAR=5

        ##Displays the Words "BEST PLAY" and its equivalent value.
        self.labelBEST = Label(self.Right, text = "Best Play", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelBEST.grid(row=1, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelBESTValue = Label(self.Right, textvariable=best_play, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=font_color,bg=darkgray )
        self.labelBESTValue.grid(row=1, column=1, padx=5, pady=2.5, sticky = 'W')

        ##Displays the word "PORT CHANGE" and its equivalent value.
        self.labelBEST_CHANGE = Label(self.Right, text = "Port Change", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelBEST_CHANGE.grid(row=2, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelBEST_CHANGE  = Label(self.Right,textvariable = best_change , font = ('Helvetica', 12, 'bold'), width = midwidth, fg=font_color,bg=darkgray )
        self.labelBEST_CHANGE.grid(row=2, column=1, padx=5, pady=2.5, sticky = 'W')

        #Spacing
        self.labelNOTHING = Label(self.Right, text = "---------------------------------------------", font = ('Helvetica', 4, 'bold'), fg=gray,bg=blackcellphone )#DividingLine
        self.labelNOTHING.grid(row=3, column=0,columnspan=2)

        ##Displays the Words "WORST PLAY" and its equivalent value.
        self.labelWORST = Label(self.Right, text = "Worst Play", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone)
        self.labelWORST.grid(row=4, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelWORSTValue = Label(self.Right, textvariable = worst_play, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=font_color, bg=darkgray)
        self.labelWORSTValue.grid(row=4, column=1, padx=5, pady=2.5, sticky = 'W',columnspan=2)

        ##Displays the word "PORT CHANGE" and its equivalent value.
        self.labelWORST_CHANGE = Label(self.Right, text = "Port Change", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelWORST_CHANGE.grid(row=5, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelWORST_CHANGE = Label(self.Right, textvariable = worst_change, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=font_color,bg=darkgray)
        self.labelWORST_CHANGE.grid(row=5, column=1, padx=5, pady=2.5, sticky = 'W')

        #Spacing
        self.labelNOTHING = Label(self.Right, text = "---------------------------------------------", font = ('Helvetica', 4, 'bold'), fg=gray,bg=blackcellphone )#DividingLine
        self.labelNOTHING.grid(row=6, column=0,columnspan=2)
              
        ####RATIOS####

        ##Displays the word "HIT PERCENTAGE" and its equivalent value.
        self.labelHIT = Label(self.Right, text = "Hit Percentage", font = ('Helvetica', 12, 'bold'), fg=font_color, bg=blackcellphone)
        self.labelHIT.grid(row=7, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelHITValue = Label(self.Right, textvariable =hit_ratio, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=font_color,bg=statsfade, anchor='w' )
        self.labelHITValue.grid(row=7, column=1, padx=5, pady=2.5, sticky = 'W')

        ##Displays the word "AVERAGE EXPECTANCY" and its equivalent value.
        self.labelEXPECTANCY = Label(self.Right, text = "Expecancy", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelEXPECTANCY.grid(row=8, column=0, padx=padxVAR, pady=0, sticky = 'W')
        self.labelEXPECTANCYValue = Label(self.Right, textvariable = expectancy, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=font_color,bg=statsfade, anchor='w')
        self.labelEXPECTANCYValue.grid(row=8, column=1, padx=5, pady=2.5, sticky = 'W')

        #Spacing
        self.labelNOTHING = Label(self.Right, text = "---------------------------------------------", font = ('Helvetica', 4, 'bold'), fg=gray,bg=blackcellphone )#DividingLine
        self.labelNOTHING.grid(row=9, column=0,columnspan=2)

        #####OUTCOME####

        ##Displays the word "TOTAL GAIN" and its equivalent value.
        self.labelTOTAL = Label(self.Right, text = "Total Gain", font = ('Helvetica', 12, 'bold'), fg=font_color, bg=blackcellphone)
        self.labelTOTAL.grid(row=10, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelTOTALValue = Label(self.Right, textvariable=total_gain, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=blackcellphone,bg=green )
        self.labelTOTALValue.grid(row=10, column=1, padx=5, pady=2.5, sticky = 'W')

        ##Displays the word "AVERAGE GAIN" and its equivalent value.
        self.labelGAIN = Label(self.Right, text = "Average Gain", font = ('Helvetica', 12, 'bold'), fg=font_color, bg=blackcellphone)
        self.labelGAIN.grid(row=11, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelGAINValue = Label(self.Right, textvariable = average_gain, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=blackcellphone,bg=gold)
        self.labelGAINValue.grid(row=11, column=1, padx=5, pady=2.5, sticky = 'W')

        ##Displays the word "AVERAGE LOSS" and its equivalent value.
        self.labelLOSS = Label(self.Right, text = "Average Loss", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelLOSS.grid(row=12, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelLOSSValue = Label(self.Right, textvariable = average_loss, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=font_color,bg=rose)
        self.labelLOSSValue.grid(row=12, column=1, padx=5, pady=2.5, sticky = 'W')

        ##Displays the word "LARGEST GAIN" and its equivalent value.
        self.labelLARGEGAIN = Label(self.Right, text = "Largest Gain", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelLARGEGAIN.grid(row=13, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelLARGEGAINValue = Label(self.Right, textvariable = largest_gain, font = ('Helvetica', 12, 'bold'), width = midwidth,fg=font_color,bg=darkgray)
        self.labelLARGEGAINValue.grid(row=13, column=1, padx=5, pady=2.5, sticky = 'W')

        ##Displays the word "LARGEST LOSS" and its equivalent value.
        self.labelLARGELOSS = Label(self.Right, text = "Largest Loss", font = ('Helvetica', 12, 'bold'), fg=font_color, bg=blackcellphone)
        self.labelLARGELOSS.grid(row=14, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelLARGELOSSValue = Label(self.Right, textvariable = largest_loss, font = ('Helvetica', 12, 'bold'), width =midwidth, fg=font_color,bg=darkgray)
        self.labelLARGELOSSValue.grid(row=14, column=1, padx=5, pady=2.5, sticky = 'W')

        #Spacing
        self.labelNOTHING = Label(self.Right, text = "---------------------------------------------", font = ('Helvetica', 4, 'bold'), fg=gray,bg=blackcellphone )#DividingLine
        self.labelNOTHING.grid(row=15, column=0,columnspan=2)
        
        ####OTHERS#####

        ##Displays the word "LONGEST HOLD" and its equivalent value.
        self.labelLONGESTHOLD = Label(self.Right, text = "Longest Hold", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelLONGESTHOLD.grid(row=16, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelLONGESTHOLDValue = Label(self.Right, textvariable = longest_hold, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=font_color,bg=blackcellphone,anchor='w')
        self.labelLONGESTHOLDValue.grid(row=16, column=1, padx=5, pady=2.5, sticky = 'W')

        ##Displays the word "AVERAGE HOLD" and its equivalent value.
        self.labelHOLD = Label(self.Right, text = "Average Hold", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelHOLD.grid(row=17, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelHOLDValue = Label(self.Right, textvariable = average_hold, font = ('Helvetica', 12, 'bold'), width = midwidth, fg=font_color,bg=blackcellphone,anchor='w')
        self.labelHOLDValue.grid(row=17, column=1, padx=5, pady=2.5, sticky = 'W')

        ##Displays the word "AVERAGE RISK" and its equivalent value.
        self.labelRISK = Label(self.Right, text = "Average Risk", font = ('Helvetica', 12, 'bold'), fg=font_color,bg=blackcellphone )
        self.labelRISK.grid(row=18, column=0, padx=padxVAR, pady=2.5, sticky = 'W')
        self.labelRISKValue = Label(self.Right, textvariable = average_risk, font = ('Helvetica', 12, 'bold'), width =midwidth, fg=font_color,bg=blackcellphone,anchor='w')
        self.labelRISKValue.grid(row=18, column=1, padx=5, pady=2.5, sticky = 'W')
    
    #========================================================================BUTTONS=====================================================================#
        
        ##Displays the button "ADD"
        self.buttonADD = Button(self.ButtonsFrame, text = "ADD", font = ('Helvetica', 16, 'bold'), fg=font_color, bg=darkgreen,width=14,command=AddTrade)
        self.buttonADD.grid(row=0, column=0,pady=6,padx=5)

        ##Displays the button "CLEAR"
        self.buttonClear = Button(self.ButtonsFrame, text = "CLEAR", font = ('Helvetica', 16, 'bold'), fg=font_color, bg=buttons_color,width=14,command=Clear)
        self.buttonClear.grid(row=0, column=1,pady=6,padx=5)

        ##Displays the button "SEARCH"
        self.buttonSEARCH = Button(self.ButtonsFrame, text = "SEARCH", font = ('Helvetica', 16, 'bold'), fg=font_color, bg=buttons_color,width=14,command=SearchTrade)
        self.buttonSEARCH.grid(row=0, column=2,pady=6,padx=5)

        ##Displays the button "REPLACE"
        self.buttonREPLACE = Button(self.ButtonsFrame, text = "REPLACE", font = ('Helvetica', 16, 'bold'), fg=font_color, bg=buttons_color,width=14,command=UpdateTrade)
        self.buttonREPLACE.grid(row=0, column=3,pady=6,padx=5)

        ##Displays the button "FORMAT" 
        self.buttonFORMAT = Button(self.ButtonsFrame, text = "FORMAT", font = ('Helvetica', 16, 'bold'), fg=font_color, bg=buttons_color,width=14,command=FormatTable)
        self.buttonFORMAT.grid(row=0, column=4,pady=6,padx=5)

        ##Displays the button "SAVE"
        self.buttonSAVE = Button(self.ButtonsFrame, text = "SAVE / EXIT", font = ('Helvetica', 16, 'bold'), fg=font_color, bg=rose,width=13,command=ExitJournal)
        self.buttonSAVE.grid(row=0, column=5,pady=6,padx=5)
        

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$_RUN ON START UP_$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
    #                                                                                                                                       #
    #                                                                                                                                       #  
        TradeData()#CHECKS if the User have a saved Database. If there is none, create one.
        
        Refresh()#RECALCULATE every Stats and Graphs then show them to the User.
        
        Set_SavedVAR()#UPDATE currentCapital varible with the value the User saved last session.
    #                                                                                                                                       #
    #                                                                                                                                       #        
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$_RUN ON START UP_$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#
        

##DISPLAY the Interface to the User
if __name__ =='__main__':
        root = Tk()
        application = OpenJournal(root)
        root= mainloop()      

    #~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~__CONTRIBUTORS__~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~0~#
    #                                                                                                                                       #
    #                                                                                                                                       #
    #                                                      AKASHIN        &         CHEN C.                                                 #
    #                                                                                                                                       #
    #                                                                                                                                       #        
    #~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~__(2022)__~~~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0~~0~0~0_#


#1.1 Update
    #New Feature. Added Entry and Exit psychological noting. ("Tilt","Fear","Neutral","Fomo","Euphoria")
    #New Feature. Added scrollbar widget. Laptops and similar devices no longer require mouse in navigating records.
    #New Feature. Search by Entry and Exit psy-state is supported. (Also, search by date no longer requires additional entries like Stock or Play.)
    #Optimization. Removed temp, os module. (No longer intending to use these modules on future versions.)
    #Bug Fix. Middle mouse button now scrolls the Treeview up and down as intended.
    #Bug Fix. Factory Reset now includes setting saved ('pickled') variable to default(zero).
    
    
    


    
