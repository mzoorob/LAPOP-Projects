Sub GetDistricts2()
'
' GetDistricts2 Macro
'
' Keyboard Shortcut: Ctrl+Shift+G
'
    lastRow& = Range("B" & Rows.Count).End(xlUp).Row
    ActiveCell.FormulaR1C1 = "=SUM(R2C2:RC[-2])"
    Range("D2").Select
    Selection.AutoFill Destination:=Range("D2:D" & lastRow&)
    Range("E2").Select
    ActiveCell.FormulaR1C1 = "=ROUND(MAX(C[-1])/RC[-2], 0)"
    Range("F2").Select
    ActiveCell.FormulaR1C1 = "=RANDBETWEEN(1, RC[-1])"
    Range("F2").Select
    Selection.Copy
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False
    Range("G2").Select
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False
    Range("G3").Select
    Application.CutCopyMode = False
    ActiveCell.FormulaR1C1 = "=R[-1]C+R2C[-2]"
    Range("G3").Select
    Selection.AutoFill Destination:=Range("G3:G" & lastRow&)
    Range("H2").Select
    Selection.FormulaArray = "=MIN(IF(C[-4]>RC[-1],C[-4],"" ""))"
    Selection.AutoFill Destination:=Range("H2:H" & lastRow&)
    Range("I2").Select
    ActiveCell.FormulaR1C1 = "=INDEX(C[-8], MATCH(RC[-1],C[-5], 0))"
    Range("I2").Select
    Selection.AutoFill Destination:=Range("I2:I" & lastRow&)
    Dim lastRow2 As Long
    With ActiveSheet
       lastRow2 = .Range("I" & .Rows.Count).End(xlUp).Row
    End With
    For i = lastRow2 To 1 Step -1
        If Cells(i, "I").Text <> "#N/A" Then
            Exit For
        End If
    Next i
    lastRow = i
    Range(Cells(2, 9), Cells(lastRow, 9)).Select
End Sub
