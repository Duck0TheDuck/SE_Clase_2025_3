--PASO 1
CREATE DATABASE [BD_UNIDAD_4_SE_2025_1]

USE BD_UNIDAD_4_SE_2025_1
GO

--DROP TABLE devices_info
--PASO 2
CREATE TABLE [dbo].[devices_info](
    [id_device] [numeric](18, 0) IDENTITY(1,1) NOT NULL,
    [id_type] [numeric](18, 0) NOT NULL, --SENSOR O ACTUADOR
    [id_signal_type] [numeric](18, 0) NOT NULL, -- DIGITAL O ANALOGICO
    [name] [nvarchar](100) NOT NULL,     
    [vendor] [nvarchar](100) NOT NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[devices_info] ADD PRIMARY KEY CLUSTERED 
(
    [id_device] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]

BEGIN TRAN
INSERT INTO devices_info (NAME, VENDOR, id_type, id_signal_type) VALUES('SENSOR DE DISTANCIA','SE_CLASE', 1, 1)
INSERT INTO devices_info (NAME, VENDOR, id_type, id_signal_type) VALUES('SENSOR DE PROXIMIDAD','SE_CLASE', 1, 1)
SELECT * FROM devices_info
ROLLBACK TRAN

INSERT INTO devices_info (NAME, VENDOR, id_type, id_signal_type) VALUES('SENSOR DE PRESENCIA','SE_CLASE', 1, 1)
SELECT * FROM devices_info

GO

--PASO 3
CREATE TABLE [dbo].[devices_records](  -- HISTORICO ---> DW  ---> EDA (ANALISIS EXPLORATORIO DE DATOS)
    [id_record] [numeric](18, 0) IDENTITY(1,1) NOT NULL,
    [id_device] [numeric](18, 0) NOT NULL,
    [current_value] [numeric](18, 0) NOT NULL,
    [date_record] [datetime] NOT NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[devices_records] ADD PRIMARY KEY CLUSTERED 
(
    [id_record] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]

GO
--PASO 4 
CREATE PROCEDURE [dbo].[SP_Insert_DevicesRecords] 
    -- Add the parameters for the stored procedure here
    @id_device as numeric(18,0), 
    @current_value as numeric(18,0)  -- va (VALOR ACTUAL)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;

    INSERT INTO [dbo].[devices_records]
           ([id_device]
            ,[date_record]
            ,[current_value]
           )
     VALUES
           (@id_device
            ,GETDATE()
           ,@current_value
           )
    
END


---PASO 5
exec SP_Insert_DevicesRecords 1, 120
exec SP_Insert_DevicesRecords 1, 240
exec SP_Insert_DevicesRecords 1, 170
exec SP_Insert_DevicesRecords 1, 390
exec SP_Insert_DevicesRecords 2, 80
exec SP_Insert_DevicesRecords 2, 140
exec SP_Insert_DevicesRecords 2, 890

select * from devices_records
SELECT * FROM devices_info

UPDATE devices_records SET id_device = 5 WHERE id_device = 2

GO

CREATE PROCEDURE [dbo].[SP_SelectALL_records]
    -- Add the parameters for the stored procedure here 
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;

    SELECT DI.id_device, DI.name "NAME", DR.current_value "CURRENT_VALUE", 
    DR.date_record "DATE_RECORD"
    FROM devices_records DR
    INNER JOIN devices_info DI ON DR.id_device = DI.id_device
           
END

EXEC SP_SelectALL_records

GO

CREATE PROCEDURE [dbo].[SP_SelecLastRecordByID]
    -- Add the parameters for the stored procedure here 
    @id_device as numeric(18,0)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;
    

    SELECT TOP 1 DI.id_device, DI.name "NAME", DR.current_value "CURRENT_VALUE", 
    DR.date_record "DATE_RECORD"
    FROM devices_records DR
    INNER JOIN devices_info DI ON DR.id_device = DI.id_device
    WHERE DI.id_device = @id_device
    ORDER BY DR.date_record DESC

           
END

GO

EXEC SP_SelectALL_records
EXEC SP_SelecLastRecordByID 5

GO

--PASO 6 ****** 
CREATE TABLE [dbo].[toma_decisiones]( --"valores_optimizados"
    [id_decision] [numeric](18, 0) IDENTITY(1,1) NOT NULL,
    [velocidad] [numeric](18, 0) NOT NULL,
    [distancia] [numeric](18, 0) NOT NULL,
    [decision] [numeric](18, 0) NOT NULL,
    [date_record] [datetime] NOT NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[toma_decisiones] ADD PRIMARY KEY CLUSTERED 
(
    [id_decision] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]


--paso 7
CREATE PROCEDURE [dbo].[SP_Insert_Decision] 
    -- Add the parameters for the stored procedure here        
    @velocidad as numeric(18, 0),
    @distancia as numeric(18, 0),
    @decision as numeric(18, 0)  
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;

    INSERT INTO [dbo].[toma_decisiones]
           ([velocidad]
            ,[distancia]
            ,[decision],
            [date_record]
           )
     VALUES
           (@velocidad,
           @distancia,
           @decision
            ,GETDATE()           
           )
    
END


SP_Insert_Decision 10, 20, 1
SP_Insert_Decision 20, 40, 2
SP_Insert_Decision 60, 60, 3

select * from toma_decisiones

--paso 8
CREATE PROCEDURE [dbo].[SP_SelecLastDecision]
    -- Add the parameters for the stored procedure here   
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON;

    SELECT top 1 *
    FROM toma_decisiones        
    order by date_record desc
           
END