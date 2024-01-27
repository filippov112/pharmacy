DECLARE @TableName NVARCHAR(MAX);
DECLARE @Индекс INT = 1;
DECLARE @Количество_Строк INT;
DECLARE @Список_Строк TABLE (ID INT IDENTITY(1,1), Строка NVARCHAR(100));

INSERT INTO @Список_Строк (Строка) VALUES (N'Certificate'), (N'CertificateAttachment'), (N'Contract'), (N'ContractMedicine'), (N'Doctor'), (N'LegalEntity'), (N'MedicalFacility'), (N'MedicineGroup'), (N'Order'), 
(N'OrderComposition'), (N'PhysicalPerson'), (N'PrescComposition'), (N'Prescription'), (N'Profile'), (N'Receipt'), (N'ReceiptItem'), (N'Supplier'), (N'Medicine');

SELECT @Количество_Строк = COUNT(*) FROM @Список_Строк;

WHILE @Индекс <= @Количество_Строк
BEGIN
    SELECT @TableName = Строка FROM @Список_Строк WHERE ID = @Индекс;
   
	--DECLARE @TableName NVARCHAR(MAX) = 'auth_user_groups';

	DECLARE column_cursor CURSOR FOR 
	SELECT COLUMN_NAME 
	FROM INFORMATION_SCHEMA.COLUMNS 
	WHERE TABLE_NAME = @TableName;

	DECLARE @d1 NVARCHAR(MAX) = '   ';
	DECLARE @d2 NVARCHAR(MAX) = '   ';
	DECLARE @d3 NVARCHAR(MAX) = '   ';
	DECLARE @w1 NVARCHAR(MAX) = '   ';

	DECLARE @ColumnName NVARCHAR(MAX);

	OPEN column_cursor;
	FETCH NEXT FROM column_cursor INTO @ColumnName;
	WHILE @@FETCH_STATUS = 0
	BEGIN
		SET @d1 = @d1 + 'CASE WHEN i.' + @ColumnName + ' <> d.' + @ColumnName + ' THEN ''' + @ColumnName + ':''+ CONVERT(NVARCHAR(MAX), d.' + @ColumnName + ') + ''->'' + CONVERT(NVARCHAR(MAX), i.' + @ColumnName + ') + ''; '' ELSE '''' END + ';
		SET @d2 = @d2 + 'CASE WHEN  i.' + @ColumnName + ' IS NOT NULL THEN ''' + @ColumnName + ':''+ CONVERT(NVARCHAR(MAX), i.' + @ColumnName + ') + ''; '' ELSE '''' END + ';
		SET @d3 = @d3 + 'CASE WHEN  d.' + @ColumnName + ' IS NOT NULL THEN ''' + @ColumnName + ':''+ CONVERT(NVARCHAR(MAX), d.' + @ColumnName + ') + ''; '' ELSE '''' END + ';
		SET @w1 = @w1 + 'd.' + @ColumnName + ' <> i.' + @ColumnName + ' or ';
		FETCH NEXT FROM column_cursor INTO @ColumnName;
	END
	CLOSE column_cursor;
	DEALLOCATE column_cursor;

	SET @d1 = SUBSTRING(@d1, 0, len(@d1));
	SET @d2 = SUBSTRING(@d2, 0, len(@d2));
	SET @d3 = SUBSTRING(@d3, 0, len(@d3));
	SET @w1 = SUBSTRING(@w1, 0, len(@w1)-1);

	DECLARE @REQUEST NVARCHAR(MAX) = '
	CREATE TRIGGER UniversalLogTrigger_'+@TableName+'
	ON dbo."'+@TableName+'"
	AFTER UPDATE, INSERT, DELETE
	AS
	BEGIN
	
		DECLARE @IsDelete BIT = ''false'';
		DECLARE @IsInsert BIT = ''false'';
		IF EXISTS (SELECT * FROM deleted) 
		BEGIN
			SET @IsDelete = ''true'';
		END
		IF EXISTS (SELECT * FROM inserted) 
		BEGIN
			SET @IsInsert = ''true'';
		END
	

		DECLARE @EventType NVARCHAR(50);
		DECLARE @RecordID INT;
		IF @IsDelete = ''true'' AND @IsInsert = ''true''
		BEGIN
			SET @EventType = ''Update'';
			SELECT @RecordID = id FROM deleted;
		END
		ELSE IF @IsInsert = ''true''
		BEGIN
			SET @EventType = ''Insert'';
			SELECT @RecordID = id FROM inserted;
		END
		ELSE IF @IsDelete = ''true''
		BEGIN
			SET @EventType = ''Delete'';
			SELECT @RecordID = id FROM deleted;
		END
	

		DECLARE @EventDateTime DATETIME = GETDATE();
		IF @IsInsert = ''true'' AND @IsDelete = ''true''
		BEGIN
			INSERT INTO dbo.Logs (TableName, EventDateTime, EventType, RecordID, Details) 
			SELECT '''+@TableName+''', @EventDateTime, @EventType, @recordID, ' + @d1 + ' 
			FROM inserted i 
			INNER JOIN deleted d ON i.id = d.id
			WHERE '+@w1+';
		END

		ELSE IF @IsInsert = ''true''
		BEGIN
			INSERT INTO dbo.Logs (TableName, EventDateTime, EventType, RecordID, Details) 
			SELECT '''+@TableName+''', @EventDateTime, @EventType, @recordID, ' + @d2 + ' FROM inserted i;
		END

		ELSE IF @IsDelete = ''true''
		BEGIN
			INSERT INTO dbo.Logs (TableName, EventDateTime, EventType, RecordID, Details) 
			SELECT '''+@TableName+''', @EventDateTime, @EventType, @recordID, ' + @d3 + ' FROM deleted d;
		END

	END
	';

	--select @REQUEST;
	EXEC sp_executesql @REQUEST;

    SET @Индекс = @Индекс + 1;
END;
