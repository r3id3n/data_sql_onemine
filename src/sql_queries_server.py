QUERIES_SERVER = {
"Consulta Cartir del día": 
"""--Cartier del día
SELECT TOP (1) 
CartirId,
Name,
CAST (CartirDate AS smalldatetime) AS CartirDate,
CAST (CreatedAt AS smalldatetime) AS CreatedAt,
CAST (UpdatedAt AS smalldatetime) AS UpdatedAt
FROM Cartir ORDER BY CartirId DESC;

-- Total de cartir cargado en turno
WITH LatestCartir AS (
    -- Obtener el CartirId más reciente
    SELECT TOP (1) 
        CartirId
    FROM Cartir
    ORDER BY CartirId DESC
)
-- Usar el CartirId obtenido en la siguiente consulta
SELECT
    t.CartirId,
    'Turno A' AS ShiftId,
    -- Suma de los programado
    SUM(t.PailQuantity) AS Total,
    -- Suma de los valores cartir
    COUNT(*) AS Ingresos
FROM Task t
INNER JOIN LatestCartir lc ON t.CartirId = lc.CartirId
WHERE t.ShiftId = 22
GROUP BY t.CartirId, t.ShiftId;
""",
#********************************************************************************************
"Consulta Listado de operadores": 
"""--Listado
DECLARE @InsertStatement NVARCHAR(MAX) = N'';

DECLARE @OperatorId INT;
DECLARE @FirstName NVARCHAR(50);
DECLARE @LastName NVARCHAR(50);
DECLARE @TagId INT;
DECLARE @SectorId INT;
DECLARE @CreatedAt DATETIME;
DECLARE @SapNumber NVARCHAR(50);

-- Crear una tabla temporal para almacenar las sentencias
CREATE TABLE #TempStatements (StatementPart NVARCHAR(MAX));

DECLARE cur CURSOR FOR
SELECT 
    OperatorId, 
    FirstName, 
    LastName, 
    TagId, 
    SectorId, 
    CreatedAt, 
    SapNumber
FROM Operator;

OPEN cur;
FETCH NEXT FROM cur INTO @OperatorId, @FirstName, @LastName, @TagId, @SectorId, @CreatedAt, @SapNumber;

WHILE @@FETCH_STATUS = 0
BEGIN
    SET @InsertStatement = 
        'INSERT INTO Operators (OperatorsId, FirstName, LastName, TagId, SectorId, CreatedAt, SapNumber) VALUES (' + 
        CAST(@OperatorId AS NVARCHAR) + ', ' +
        QUOTENAME(ISNULL(@FirstName, ''), '''') + ', ' +
        QUOTENAME(ISNULL(@LastName, ''), '''') + ', ' +
        ISNULL(CAST(@TagId AS NVARCHAR), 'NULL') + ', ' +
        ISNULL(CAST(@SectorId AS NVARCHAR), 'NULL') + ', ' +
        QUOTENAME(CONVERT(NVARCHAR, @CreatedAt, 120), '''') + ', ' +
        QUOTENAME(ISNULL(@SapNumber, ''), '''') + ');';

    -- Insertar la sentencia en la tabla temporal
    INSERT INTO #TempStatements (StatementPart) VALUES (@InsertStatement);

    FETCH NEXT FROM cur INTO @OperatorId, @FirstName, @LastName, @TagId, @SectorId, @CreatedAt, @SapNumber;
END

CLOSE cur;
DEALLOCATE cur;

-- Seleccionar todas las sentencias para copiar
SELECT * FROM #TempStatements;

-- Limpiar la tabla temporal
DROP TABLE #TempStatements;
"""

}